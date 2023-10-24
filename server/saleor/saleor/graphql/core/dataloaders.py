from collections import defaultdict
from typing import DefaultDict, Generic, Iterable, List, Optional, Tuple, TypeVar, Union

import opentracing
import opentracing.tags
from promise import Promise
from promise.dataloader import DataLoader as BaseLoader

from ...thumbnail.models import Thumbnail
from ...thumbnail.utils import get_thumbnail_format
from . import SaleorContext
from .context import get_database_connection_name

K = TypeVar("K")
R = TypeVar("R")


class DataLoader(BaseLoader, Generic[K, R]):
    context_key: str
    context: SaleorContext
    database_connection_name: str

    def __new__(cls, context: SaleorContext):
        key = cls.context_key
        if key is None:
            raise TypeError("Data loader %r does not define a context key" % (cls,))
        if not hasattr(context, "dataloaders"):
            context.dataloaders = {}
        if key not in context.dataloaders:
            context.dataloaders[key] = super().__new__(cls)
        loader = context.dataloaders[key]
        assert isinstance(loader, cls)
        return loader

    def __init__(self, context: SaleorContext) -> None:
        if getattr(self, "context", None) != context:
            self.context = context
            self.database_connection_name = get_database_connection_name(context)
            super().__init__()

    def batch_load_fn(  # pylint: disable=method-hidden
        self, keys: Iterable[K]
    ) -> Promise[List[R]]:
        with opentracing.global_tracer().start_active_span(
            self.__class__.__name__
        ) as scope:
            span = scope.span
            span.set_tag(opentracing.tags.COMPONENT, "dataloaders")
            results = self.batch_load(keys)
            if not isinstance(results, Promise):
                return Promise.resolve(results)
            return results

    def batch_load(self, keys: Iterable[K]) -> Union[Promise[List[R]], List[R]]:
        raise NotImplementedError()


class BaseThumbnailBySizeAndFormatLoader(
    DataLoader[Tuple[int, int, Optional[str]], Thumbnail]
):
    model_name: str

    def batch_load(self, keys: Iterable[Tuple[int, int, Optional[str]]]):
        model_name = self.model_name.lower()
        instance_ids = [id for id, _, _ in keys]
        lookup = {f"{model_name}_id__in": instance_ids}
        thumbnails = Thumbnail.objects.using(self.database_connection_name).filter(
            **lookup
        )
        thumbnails_by_instance_id_size_and_format_map: DefaultDict[
            Tuple[int, int, Optional[str]], Thumbnail
        ] = defaultdict()
        for thumbnail in thumbnails:
            format = get_thumbnail_format(thumbnail.format)
            thumbnails_by_instance_id_size_and_format_map[
                (getattr(thumbnail, f"{model_name}_id"), thumbnail.size, format)
            ] = thumbnail
        return [thumbnails_by_instance_id_size_and_format_map.get(key) for key in keys]
