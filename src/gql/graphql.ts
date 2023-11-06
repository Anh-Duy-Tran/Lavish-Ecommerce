/* eslint-disable */
import { TypedDocumentNode as DocumentNode } from "@graphql-typed-document-node/core";
export type Maybe<T> = T | null;
export type InputMaybe<T> = Maybe<T>;
export type Exact<T extends { [key: string]: unknown }> = {
  [K in keyof T]: T[K];
};
export type MakeOptional<T, K extends keyof T> = Omit<T, K> & {
  [SubKey in K]?: Maybe<T[SubKey]>;
};
export type MakeMaybe<T, K extends keyof T> = Omit<T, K> & {
  [SubKey in K]: Maybe<T[SubKey]>;
};
export type MakeEmpty<
  T extends { [key: string]: unknown },
  K extends keyof T,
> = { [_ in K]?: never };
export type Incremental<T> =
  | T
  | {
      [P in keyof T]?: P extends " $fragmentName" | "__typename" ? T[P] : never;
    };
/** All built-in and custom scalars, mapped to their actual values */
export type Scalars = {
  ID: { input: string; output: string };
  String: { input: string; output: string };
  Boolean: { input: boolean; output: boolean };
  Int: { input: number; output: number };
  Float: { input: number; output: number };
  /**
   * A date-time string at UTC, such as 2007-12-03T10:15:30Z,
   *     compliant with the 'date-time' format outlined in section 5.6 of
   *     the RFC 3339 profile of the ISO 8601 standard for representation
   *     of dates and times using the Gregorian calendar.
   */
  DateTime: { input: any; output: any };
  /** The 'Dimension' type represents dimensions as whole numeric values between `1` and `4000`. */
  Dimension: { input: any; output: any };
  /** The 'HexColor' type represents color in `rgb:ffffff` string format. */
  HexColor: { input: any; output: any };
  /** The 'Quality' type represents quality as whole numeric values between `1` and `100`. */
  Quality: { input: any; output: any };
};

/** Represents a binary file in a space. An asset can be any file type. */
export type Asset = {
  __typename?: "Asset";
  contentType: Maybe<Scalars["String"]["output"]>;
  contentfulMetadata: ContentfulMetadata;
  description: Maybe<Scalars["String"]["output"]>;
  fileName: Maybe<Scalars["String"]["output"]>;
  height: Maybe<Scalars["Int"]["output"]>;
  linkedFrom: Maybe<AssetLinkingCollections>;
  size: Maybe<Scalars["Int"]["output"]>;
  sys: Sys;
  title: Maybe<Scalars["String"]["output"]>;
  url: Maybe<Scalars["String"]["output"]>;
  width: Maybe<Scalars["Int"]["output"]>;
};

/** Represents a binary file in a space. An asset can be any file type. */
export type AssetContentTypeArgs = {
  locale: InputMaybe<Scalars["String"]["input"]>;
};

/** Represents a binary file in a space. An asset can be any file type. */
export type AssetDescriptionArgs = {
  locale: InputMaybe<Scalars["String"]["input"]>;
};

/** Represents a binary file in a space. An asset can be any file type. */
export type AssetFileNameArgs = {
  locale: InputMaybe<Scalars["String"]["input"]>;
};

/** Represents a binary file in a space. An asset can be any file type. */
export type AssetHeightArgs = {
  locale: InputMaybe<Scalars["String"]["input"]>;
};

/** Represents a binary file in a space. An asset can be any file type. */
export type AssetLinkedFromArgs = {
  allowedLocales: InputMaybe<Array<InputMaybe<Scalars["String"]["input"]>>>;
};

/** Represents a binary file in a space. An asset can be any file type. */
export type AssetSizeArgs = {
  locale: InputMaybe<Scalars["String"]["input"]>;
};

/** Represents a binary file in a space. An asset can be any file type. */
export type AssetTitleArgs = {
  locale: InputMaybe<Scalars["String"]["input"]>;
};

/** Represents a binary file in a space. An asset can be any file type. */
export type AssetUrlArgs = {
  locale: InputMaybe<Scalars["String"]["input"]>;
  transform: InputMaybe<ImageTransformOptions>;
};

/** Represents a binary file in a space. An asset can be any file type. */
export type AssetWidthArgs = {
  locale: InputMaybe<Scalars["String"]["input"]>;
};

export type AssetCollection = {
  __typename?: "AssetCollection";
  items: Array<Maybe<Asset>>;
  limit: Scalars["Int"]["output"];
  skip: Scalars["Int"]["output"];
  total: Scalars["Int"]["output"];
};

export type AssetFilter = {
  AND: InputMaybe<Array<InputMaybe<AssetFilter>>>;
  OR: InputMaybe<Array<InputMaybe<AssetFilter>>>;
  contentType: InputMaybe<Scalars["String"]["input"]>;
  contentType_contains: InputMaybe<Scalars["String"]["input"]>;
  contentType_exists: InputMaybe<Scalars["Boolean"]["input"]>;
  contentType_in: InputMaybe<Array<InputMaybe<Scalars["String"]["input"]>>>;
  contentType_not: InputMaybe<Scalars["String"]["input"]>;
  contentType_not_contains: InputMaybe<Scalars["String"]["input"]>;
  contentType_not_in: InputMaybe<Array<InputMaybe<Scalars["String"]["input"]>>>;
  contentfulMetadata: InputMaybe<ContentfulMetadataFilter>;
  description: InputMaybe<Scalars["String"]["input"]>;
  description_contains: InputMaybe<Scalars["String"]["input"]>;
  description_exists: InputMaybe<Scalars["Boolean"]["input"]>;
  description_in: InputMaybe<Array<InputMaybe<Scalars["String"]["input"]>>>;
  description_not: InputMaybe<Scalars["String"]["input"]>;
  description_not_contains: InputMaybe<Scalars["String"]["input"]>;
  description_not_in: InputMaybe<Array<InputMaybe<Scalars["String"]["input"]>>>;
  fileName: InputMaybe<Scalars["String"]["input"]>;
  fileName_contains: InputMaybe<Scalars["String"]["input"]>;
  fileName_exists: InputMaybe<Scalars["Boolean"]["input"]>;
  fileName_in: InputMaybe<Array<InputMaybe<Scalars["String"]["input"]>>>;
  fileName_not: InputMaybe<Scalars["String"]["input"]>;
  fileName_not_contains: InputMaybe<Scalars["String"]["input"]>;
  fileName_not_in: InputMaybe<Array<InputMaybe<Scalars["String"]["input"]>>>;
  height: InputMaybe<Scalars["Int"]["input"]>;
  height_exists: InputMaybe<Scalars["Boolean"]["input"]>;
  height_gt: InputMaybe<Scalars["Int"]["input"]>;
  height_gte: InputMaybe<Scalars["Int"]["input"]>;
  height_in: InputMaybe<Array<InputMaybe<Scalars["Int"]["input"]>>>;
  height_lt: InputMaybe<Scalars["Int"]["input"]>;
  height_lte: InputMaybe<Scalars["Int"]["input"]>;
  height_not: InputMaybe<Scalars["Int"]["input"]>;
  height_not_in: InputMaybe<Array<InputMaybe<Scalars["Int"]["input"]>>>;
  size: InputMaybe<Scalars["Int"]["input"]>;
  size_exists: InputMaybe<Scalars["Boolean"]["input"]>;
  size_gt: InputMaybe<Scalars["Int"]["input"]>;
  size_gte: InputMaybe<Scalars["Int"]["input"]>;
  size_in: InputMaybe<Array<InputMaybe<Scalars["Int"]["input"]>>>;
  size_lt: InputMaybe<Scalars["Int"]["input"]>;
  size_lte: InputMaybe<Scalars["Int"]["input"]>;
  size_not: InputMaybe<Scalars["Int"]["input"]>;
  size_not_in: InputMaybe<Array<InputMaybe<Scalars["Int"]["input"]>>>;
  sys: InputMaybe<SysFilter>;
  title: InputMaybe<Scalars["String"]["input"]>;
  title_contains: InputMaybe<Scalars["String"]["input"]>;
  title_exists: InputMaybe<Scalars["Boolean"]["input"]>;
  title_in: InputMaybe<Array<InputMaybe<Scalars["String"]["input"]>>>;
  title_not: InputMaybe<Scalars["String"]["input"]>;
  title_not_contains: InputMaybe<Scalars["String"]["input"]>;
  title_not_in: InputMaybe<Array<InputMaybe<Scalars["String"]["input"]>>>;
  url: InputMaybe<Scalars["String"]["input"]>;
  url_contains: InputMaybe<Scalars["String"]["input"]>;
  url_exists: InputMaybe<Scalars["Boolean"]["input"]>;
  url_in: InputMaybe<Array<InputMaybe<Scalars["String"]["input"]>>>;
  url_not: InputMaybe<Scalars["String"]["input"]>;
  url_not_contains: InputMaybe<Scalars["String"]["input"]>;
  url_not_in: InputMaybe<Array<InputMaybe<Scalars["String"]["input"]>>>;
  width: InputMaybe<Scalars["Int"]["input"]>;
  width_exists: InputMaybe<Scalars["Boolean"]["input"]>;
  width_gt: InputMaybe<Scalars["Int"]["input"]>;
  width_gte: InputMaybe<Scalars["Int"]["input"]>;
  width_in: InputMaybe<Array<InputMaybe<Scalars["Int"]["input"]>>>;
  width_lt: InputMaybe<Scalars["Int"]["input"]>;
  width_lte: InputMaybe<Scalars["Int"]["input"]>;
  width_not: InputMaybe<Scalars["Int"]["input"]>;
  width_not_in: InputMaybe<Array<InputMaybe<Scalars["Int"]["input"]>>>;
};

export type AssetLinkingCollections = {
  __typename?: "AssetLinkingCollections";
  entryCollection: Maybe<EntryCollection>;
  highlightSlideCollection: Maybe<HighlightSlideCollection>;
  productGroupCollection: Maybe<ProductGroupCollection>;
  productVariantCollection: Maybe<ProductVariantCollection>;
};

export type AssetLinkingCollectionsEntryCollectionArgs = {
  limit?: InputMaybe<Scalars["Int"]["input"]>;
  locale: InputMaybe<Scalars["String"]["input"]>;
  preview: InputMaybe<Scalars["Boolean"]["input"]>;
  skip?: InputMaybe<Scalars["Int"]["input"]>;
};

export type AssetLinkingCollectionsHighlightSlideCollectionArgs = {
  limit?: InputMaybe<Scalars["Int"]["input"]>;
  locale: InputMaybe<Scalars["String"]["input"]>;
  order: InputMaybe<
    Array<InputMaybe<AssetLinkingCollectionsHighlightSlideCollectionOrder>>
  >;
  preview: InputMaybe<Scalars["Boolean"]["input"]>;
  skip?: InputMaybe<Scalars["Int"]["input"]>;
};

export type AssetLinkingCollectionsProductGroupCollectionArgs = {
  limit?: InputMaybe<Scalars["Int"]["input"]>;
  locale: InputMaybe<Scalars["String"]["input"]>;
  order: InputMaybe<
    Array<InputMaybe<AssetLinkingCollectionsProductGroupCollectionOrder>>
  >;
  preview: InputMaybe<Scalars["Boolean"]["input"]>;
  skip?: InputMaybe<Scalars["Int"]["input"]>;
};

export type AssetLinkingCollectionsProductVariantCollectionArgs = {
  limit?: InputMaybe<Scalars["Int"]["input"]>;
  locale: InputMaybe<Scalars["String"]["input"]>;
  order: InputMaybe<
    Array<InputMaybe<AssetLinkingCollectionsProductVariantCollectionOrder>>
  >;
  preview: InputMaybe<Scalars["Boolean"]["input"]>;
  skip?: InputMaybe<Scalars["Int"]["input"]>;
};

export enum AssetLinkingCollectionsHighlightSlideCollectionOrder {
  HrefAsc = "href_ASC",
  HrefDesc = "href_DESC",
  NameAsc = "name_ASC",
  NameDesc = "name_DESC",
  RootCategorySlugAsc = "rootCategorySlug_ASC",
  RootCategorySlugDesc = "rootCategorySlug_DESC",
  ShouldRedirectAsc = "shouldRedirect_ASC",
  ShouldRedirectDesc = "shouldRedirect_DESC",
  SysFirstPublishedAtAsc = "sys_firstPublishedAt_ASC",
  SysFirstPublishedAtDesc = "sys_firstPublishedAt_DESC",
  SysIdAsc = "sys_id_ASC",
  SysIdDesc = "sys_id_DESC",
  SysPublishedAtAsc = "sys_publishedAt_ASC",
  SysPublishedAtDesc = "sys_publishedAt_DESC",
  SysPublishedVersionAsc = "sys_publishedVersion_ASC",
  SysPublishedVersionDesc = "sys_publishedVersion_DESC",
  ThemeAsc = "theme_ASC",
  ThemeDesc = "theme_DESC",
}

export enum AssetLinkingCollectionsProductGroupCollectionOrder {
  SysFirstPublishedAtAsc = "sys_firstPublishedAt_ASC",
  SysFirstPublishedAtDesc = "sys_firstPublishedAt_DESC",
  SysIdAsc = "sys_id_ASC",
  SysIdDesc = "sys_id_DESC",
  SysPublishedAtAsc = "sys_publishedAt_ASC",
  SysPublishedAtDesc = "sys_publishedAt_DESC",
  SysPublishedVersionAsc = "sys_publishedVersion_ASC",
  SysPublishedVersionDesc = "sys_publishedVersion_DESC",
  TypeAsc = "type_ASC",
  TypeDesc = "type_DESC",
}

export enum AssetLinkingCollectionsProductVariantCollectionOrder {
  ColorCodeAsc = "colorCode_ASC",
  ColorCodeDesc = "colorCode_DESC",
  ColorNameAsc = "colorName_ASC",
  ColorNameDesc = "colorName_DESC",
  FirstMediaInOverviewAsc = "firstMediaInOverview_ASC",
  FirstMediaInOverviewDesc = "firstMediaInOverview_DESC",
  PriceAsc = "price_ASC",
  PriceDesc = "price_DESC",
  RefAsc = "ref_ASC",
  RefDesc = "ref_DESC",
  SysFirstPublishedAtAsc = "sys_firstPublishedAt_ASC",
  SysFirstPublishedAtDesc = "sys_firstPublishedAt_DESC",
  SysIdAsc = "sys_id_ASC",
  SysIdDesc = "sys_id_DESC",
  SysPublishedAtAsc = "sys_publishedAt_ASC",
  SysPublishedAtDesc = "sys_publishedAt_DESC",
  SysPublishedVersionAsc = "sys_publishedVersion_ASC",
  SysPublishedVersionDesc = "sys_publishedVersion_DESC",
}

export enum AssetOrder {
  ContentTypeAsc = "contentType_ASC",
  ContentTypeDesc = "contentType_DESC",
  FileNameAsc = "fileName_ASC",
  FileNameDesc = "fileName_DESC",
  HeightAsc = "height_ASC",
  HeightDesc = "height_DESC",
  SizeAsc = "size_ASC",
  SizeDesc = "size_DESC",
  SysFirstPublishedAtAsc = "sys_firstPublishedAt_ASC",
  SysFirstPublishedAtDesc = "sys_firstPublishedAt_DESC",
  SysIdAsc = "sys_id_ASC",
  SysIdDesc = "sys_id_DESC",
  SysPublishedAtAsc = "sys_publishedAt_ASC",
  SysPublishedAtDesc = "sys_publishedAt_DESC",
  SysPublishedVersionAsc = "sys_publishedVersion_ASC",
  SysPublishedVersionDesc = "sys_publishedVersion_DESC",
  UrlAsc = "url_ASC",
  UrlDesc = "url_DESC",
  WidthAsc = "width_ASC",
  WidthDesc = "width_DESC",
}

/** Aggregate category [See type definition](https://app.contentful.com/spaces/nh559twm3d3o/content_types/categories) */
export type Categories = Entry & {
  __typename?: "Categories";
  categoriesCollection: Maybe<CategoriesCategoriesCollection>;
  contentfulMetadata: ContentfulMetadata;
  linkedFrom: Maybe<CategoriesLinkingCollections>;
  name: Maybe<Scalars["String"]["output"]>;
  sys: Sys;
};

/** Aggregate category [See type definition](https://app.contentful.com/spaces/nh559twm3d3o/content_types/categories) */
export type CategoriesCategoriesCollectionArgs = {
  limit?: InputMaybe<Scalars["Int"]["input"]>;
  locale: InputMaybe<Scalars["String"]["input"]>;
  order: InputMaybe<Array<InputMaybe<CategoriesCategoriesCollectionOrder>>>;
  preview: InputMaybe<Scalars["Boolean"]["input"]>;
  skip?: InputMaybe<Scalars["Int"]["input"]>;
  where: InputMaybe<CategoryFilter>;
};

/** Aggregate category [See type definition](https://app.contentful.com/spaces/nh559twm3d3o/content_types/categories) */
export type CategoriesLinkedFromArgs = {
  allowedLocales: InputMaybe<Array<InputMaybe<Scalars["String"]["input"]>>>;
};

/** Aggregate category [See type definition](https://app.contentful.com/spaces/nh559twm3d3o/content_types/categories) */
export type CategoriesNameArgs = {
  locale: InputMaybe<Scalars["String"]["input"]>;
};

export type CategoriesCategoriesCollection = {
  __typename?: "CategoriesCategoriesCollection";
  items: Array<Maybe<Category>>;
  limit: Scalars["Int"]["output"];
  skip: Scalars["Int"]["output"];
  total: Scalars["Int"]["output"];
};

export enum CategoriesCategoriesCollectionOrder {
  AutoFillSchemaAsc = "autoFillSchema_ASC",
  AutoFillSchemaDesc = "autoFillSchema_DESC",
  DisplayNameAsc = "displayName_ASC",
  DisplayNameDesc = "displayName_DESC",
  IsRootCategoryAsc = "isRootCategory_ASC",
  IsRootCategoryDesc = "isRootCategory_DESC",
  NameAsc = "name_ASC",
  NameDesc = "name_DESC",
  SlugAsc = "slug_ASC",
  SlugDesc = "slug_DESC",
  SysFirstPublishedAtAsc = "sys_firstPublishedAt_ASC",
  SysFirstPublishedAtDesc = "sys_firstPublishedAt_DESC",
  SysIdAsc = "sys_id_ASC",
  SysIdDesc = "sys_id_DESC",
  SysPublishedAtAsc = "sys_publishedAt_ASC",
  SysPublishedAtDesc = "sys_publishedAt_DESC",
  SysPublishedVersionAsc = "sys_publishedVersion_ASC",
  SysPublishedVersionDesc = "sys_publishedVersion_DESC",
}

export type CategoriesCollection = {
  __typename?: "CategoriesCollection";
  items: Array<Maybe<Categories>>;
  limit: Scalars["Int"]["output"];
  skip: Scalars["Int"]["output"];
  total: Scalars["Int"]["output"];
};

export type CategoriesFilter = {
  AND: InputMaybe<Array<InputMaybe<CategoriesFilter>>>;
  OR: InputMaybe<Array<InputMaybe<CategoriesFilter>>>;
  categories: InputMaybe<CfCategoryNestedFilter>;
  categoriesCollection_exists: InputMaybe<Scalars["Boolean"]["input"]>;
  contentfulMetadata: InputMaybe<ContentfulMetadataFilter>;
  name: InputMaybe<Scalars["String"]["input"]>;
  name_contains: InputMaybe<Scalars["String"]["input"]>;
  name_exists: InputMaybe<Scalars["Boolean"]["input"]>;
  name_in: InputMaybe<Array<InputMaybe<Scalars["String"]["input"]>>>;
  name_not: InputMaybe<Scalars["String"]["input"]>;
  name_not_contains: InputMaybe<Scalars["String"]["input"]>;
  name_not_in: InputMaybe<Array<InputMaybe<Scalars["String"]["input"]>>>;
  sys: InputMaybe<SysFilter>;
};

export type CategoriesLinkingCollections = {
  __typename?: "CategoriesLinkingCollections";
  entryCollection: Maybe<EntryCollection>;
};

export type CategoriesLinkingCollectionsEntryCollectionArgs = {
  limit?: InputMaybe<Scalars["Int"]["input"]>;
  locale: InputMaybe<Scalars["String"]["input"]>;
  preview: InputMaybe<Scalars["Boolean"]["input"]>;
  skip?: InputMaybe<Scalars["Int"]["input"]>;
};

export enum CategoriesOrder {
  NameAsc = "name_ASC",
  NameDesc = "name_DESC",
  SysFirstPublishedAtAsc = "sys_firstPublishedAt_ASC",
  SysFirstPublishedAtDesc = "sys_firstPublishedAt_DESC",
  SysIdAsc = "sys_id_ASC",
  SysIdDesc = "sys_id_DESC",
  SysPublishedAtAsc = "sys_publishedAt_ASC",
  SysPublishedAtDesc = "sys_publishedAt_DESC",
  SysPublishedVersionAsc = "sys_publishedVersion_ASC",
  SysPublishedVersionDesc = "sys_publishedVersion_DESC",
}

/** App category [See type definition](https://app.contentful.com/spaces/nh559twm3d3o/content_types/category) */
export type Category = Entry & {
  __typename?: "Category";
  autoFillSchema: Maybe<Scalars["String"]["output"]>;
  contentfulMetadata: ContentfulMetadata;
  customProductGroupCollection: Maybe<CategoryCustomProductGroupCollection>;
  displayName: Maybe<Scalars["String"]["output"]>;
  intersectAttributesCollection: Maybe<CategoryIntersectAttributesCollection>;
  isRootCategory: Maybe<Scalars["Boolean"]["output"]>;
  linkedFrom: Maybe<CategoryLinkingCollections>;
  name: Maybe<Scalars["String"]["output"]>;
  slug: Maybe<Scalars["String"]["output"]>;
  subCategoriesCollection: Maybe<CategorySubCategoriesCollection>;
  sys: Sys;
  unionAttributesCollection: Maybe<CategoryUnionAttributesCollection>;
};

/** App category [See type definition](https://app.contentful.com/spaces/nh559twm3d3o/content_types/category) */
export type CategoryAutoFillSchemaArgs = {
  locale: InputMaybe<Scalars["String"]["input"]>;
};

/** App category [See type definition](https://app.contentful.com/spaces/nh559twm3d3o/content_types/category) */
export type CategoryCustomProductGroupCollectionArgs = {
  limit?: InputMaybe<Scalars["Int"]["input"]>;
  locale: InputMaybe<Scalars["String"]["input"]>;
  order: InputMaybe<
    Array<InputMaybe<CategoryCustomProductGroupCollectionOrder>>
  >;
  preview: InputMaybe<Scalars["Boolean"]["input"]>;
  skip?: InputMaybe<Scalars["Int"]["input"]>;
  where: InputMaybe<ProductGroupFilter>;
};

/** App category [See type definition](https://app.contentful.com/spaces/nh559twm3d3o/content_types/category) */
export type CategoryDisplayNameArgs = {
  locale: InputMaybe<Scalars["String"]["input"]>;
};

/** App category [See type definition](https://app.contentful.com/spaces/nh559twm3d3o/content_types/category) */
export type CategoryIntersectAttributesCollectionArgs = {
  limit?: InputMaybe<Scalars["Int"]["input"]>;
  locale: InputMaybe<Scalars["String"]["input"]>;
  order: InputMaybe<
    Array<InputMaybe<CategoryIntersectAttributesCollectionOrder>>
  >;
  preview: InputMaybe<Scalars["Boolean"]["input"]>;
  skip?: InputMaybe<Scalars["Int"]["input"]>;
  where: InputMaybe<ProductAttributeFilter>;
};

/** App category [See type definition](https://app.contentful.com/spaces/nh559twm3d3o/content_types/category) */
export type CategoryIsRootCategoryArgs = {
  locale: InputMaybe<Scalars["String"]["input"]>;
};

/** App category [See type definition](https://app.contentful.com/spaces/nh559twm3d3o/content_types/category) */
export type CategoryLinkedFromArgs = {
  allowedLocales: InputMaybe<Array<InputMaybe<Scalars["String"]["input"]>>>;
};

/** App category [See type definition](https://app.contentful.com/spaces/nh559twm3d3o/content_types/category) */
export type CategoryNameArgs = {
  locale: InputMaybe<Scalars["String"]["input"]>;
};

/** App category [See type definition](https://app.contentful.com/spaces/nh559twm3d3o/content_types/category) */
export type CategorySlugArgs = {
  locale: InputMaybe<Scalars["String"]["input"]>;
};

/** App category [See type definition](https://app.contentful.com/spaces/nh559twm3d3o/content_types/category) */
export type CategorySubCategoriesCollectionArgs = {
  limit?: InputMaybe<Scalars["Int"]["input"]>;
  locale: InputMaybe<Scalars["String"]["input"]>;
  order: InputMaybe<Array<InputMaybe<CategorySubCategoriesCollectionOrder>>>;
  preview: InputMaybe<Scalars["Boolean"]["input"]>;
  skip?: InputMaybe<Scalars["Int"]["input"]>;
  where: InputMaybe<CategoryFilter>;
};

/** App category [See type definition](https://app.contentful.com/spaces/nh559twm3d3o/content_types/category) */
export type CategoryUnionAttributesCollectionArgs = {
  limit?: InputMaybe<Scalars["Int"]["input"]>;
  locale: InputMaybe<Scalars["String"]["input"]>;
  order: InputMaybe<Array<InputMaybe<CategoryUnionAttributesCollectionOrder>>>;
  preview: InputMaybe<Scalars["Boolean"]["input"]>;
  skip?: InputMaybe<Scalars["Int"]["input"]>;
  where: InputMaybe<ProductAttributeFilter>;
};

export type CategoryCollection = {
  __typename?: "CategoryCollection";
  items: Array<Maybe<Category>>;
  limit: Scalars["Int"]["output"];
  skip: Scalars["Int"]["output"];
  total: Scalars["Int"]["output"];
};

export type CategoryCustomProductGroupCollection = {
  __typename?: "CategoryCustomProductGroupCollection";
  items: Array<Maybe<ProductGroup>>;
  limit: Scalars["Int"]["output"];
  skip: Scalars["Int"]["output"];
  total: Scalars["Int"]["output"];
};

export enum CategoryCustomProductGroupCollectionOrder {
  SysFirstPublishedAtAsc = "sys_firstPublishedAt_ASC",
  SysFirstPublishedAtDesc = "sys_firstPublishedAt_DESC",
  SysIdAsc = "sys_id_ASC",
  SysIdDesc = "sys_id_DESC",
  SysPublishedAtAsc = "sys_publishedAt_ASC",
  SysPublishedAtDesc = "sys_publishedAt_DESC",
  SysPublishedVersionAsc = "sys_publishedVersion_ASC",
  SysPublishedVersionDesc = "sys_publishedVersion_DESC",
  TypeAsc = "type_ASC",
  TypeDesc = "type_DESC",
}

export type CategoryFilter = {
  AND: InputMaybe<Array<InputMaybe<CategoryFilter>>>;
  OR: InputMaybe<Array<InputMaybe<CategoryFilter>>>;
  autoFillSchema: InputMaybe<Scalars["String"]["input"]>;
  autoFillSchema_contains: InputMaybe<Scalars["String"]["input"]>;
  autoFillSchema_exists: InputMaybe<Scalars["Boolean"]["input"]>;
  autoFillSchema_in: InputMaybe<Array<InputMaybe<Scalars["String"]["input"]>>>;
  autoFillSchema_not: InputMaybe<Scalars["String"]["input"]>;
  autoFillSchema_not_contains: InputMaybe<Scalars["String"]["input"]>;
  autoFillSchema_not_in: InputMaybe<
    Array<InputMaybe<Scalars["String"]["input"]>>
  >;
  contentfulMetadata: InputMaybe<ContentfulMetadataFilter>;
  customProductGroup: InputMaybe<CfProductGroupNestedFilter>;
  customProductGroupCollection_exists: InputMaybe<Scalars["Boolean"]["input"]>;
  displayName: InputMaybe<Scalars["String"]["input"]>;
  displayName_contains: InputMaybe<Scalars["String"]["input"]>;
  displayName_exists: InputMaybe<Scalars["Boolean"]["input"]>;
  displayName_in: InputMaybe<Array<InputMaybe<Scalars["String"]["input"]>>>;
  displayName_not: InputMaybe<Scalars["String"]["input"]>;
  displayName_not_contains: InputMaybe<Scalars["String"]["input"]>;
  displayName_not_in: InputMaybe<Array<InputMaybe<Scalars["String"]["input"]>>>;
  intersectAttributes: InputMaybe<CfProductAttributeNestedFilter>;
  intersectAttributesCollection_exists: InputMaybe<Scalars["Boolean"]["input"]>;
  isRootCategory: InputMaybe<Scalars["Boolean"]["input"]>;
  isRootCategory_exists: InputMaybe<Scalars["Boolean"]["input"]>;
  isRootCategory_not: InputMaybe<Scalars["Boolean"]["input"]>;
  name: InputMaybe<Scalars["String"]["input"]>;
  name_contains: InputMaybe<Scalars["String"]["input"]>;
  name_exists: InputMaybe<Scalars["Boolean"]["input"]>;
  name_in: InputMaybe<Array<InputMaybe<Scalars["String"]["input"]>>>;
  name_not: InputMaybe<Scalars["String"]["input"]>;
  name_not_contains: InputMaybe<Scalars["String"]["input"]>;
  name_not_in: InputMaybe<Array<InputMaybe<Scalars["String"]["input"]>>>;
  slug: InputMaybe<Scalars["String"]["input"]>;
  slug_contains: InputMaybe<Scalars["String"]["input"]>;
  slug_exists: InputMaybe<Scalars["Boolean"]["input"]>;
  slug_in: InputMaybe<Array<InputMaybe<Scalars["String"]["input"]>>>;
  slug_not: InputMaybe<Scalars["String"]["input"]>;
  slug_not_contains: InputMaybe<Scalars["String"]["input"]>;
  slug_not_in: InputMaybe<Array<InputMaybe<Scalars["String"]["input"]>>>;
  subCategories: InputMaybe<CfCategoryNestedFilter>;
  subCategoriesCollection_exists: InputMaybe<Scalars["Boolean"]["input"]>;
  sys: InputMaybe<SysFilter>;
  unionAttributes: InputMaybe<CfProductAttributeNestedFilter>;
  unionAttributesCollection_exists: InputMaybe<Scalars["Boolean"]["input"]>;
};

/** [See type definition](https://app.contentful.com/spaces/nh559twm3d3o/content_types/categoryHighlight) */
export type CategoryHighlight = Entry & {
  __typename?: "CategoryHighlight";
  category: Maybe<Category>;
  contentfulMetadata: ContentfulMetadata;
  highlightSlidesCollection: Maybe<CategoryHighlightHighlightSlidesCollection>;
  linkedFrom: Maybe<CategoryHighlightLinkingCollections>;
  rootCategoryName: Maybe<Scalars["String"]["output"]>;
  sys: Sys;
};

/** [See type definition](https://app.contentful.com/spaces/nh559twm3d3o/content_types/categoryHighlight) */
export type CategoryHighlightCategoryArgs = {
  locale: InputMaybe<Scalars["String"]["input"]>;
  preview: InputMaybe<Scalars["Boolean"]["input"]>;
  where: InputMaybe<CategoryFilter>;
};

/** [See type definition](https://app.contentful.com/spaces/nh559twm3d3o/content_types/categoryHighlight) */
export type CategoryHighlightHighlightSlidesCollectionArgs = {
  limit?: InputMaybe<Scalars["Int"]["input"]>;
  locale: InputMaybe<Scalars["String"]["input"]>;
  order: InputMaybe<
    Array<InputMaybe<CategoryHighlightHighlightSlidesCollectionOrder>>
  >;
  preview: InputMaybe<Scalars["Boolean"]["input"]>;
  skip?: InputMaybe<Scalars["Int"]["input"]>;
  where: InputMaybe<HighlightSlideFilter>;
};

/** [See type definition](https://app.contentful.com/spaces/nh559twm3d3o/content_types/categoryHighlight) */
export type CategoryHighlightLinkedFromArgs = {
  allowedLocales: InputMaybe<Array<InputMaybe<Scalars["String"]["input"]>>>;
};

/** [See type definition](https://app.contentful.com/spaces/nh559twm3d3o/content_types/categoryHighlight) */
export type CategoryHighlightRootCategoryNameArgs = {
  locale: InputMaybe<Scalars["String"]["input"]>;
};

export type CategoryHighlightCollection = {
  __typename?: "CategoryHighlightCollection";
  items: Array<Maybe<CategoryHighlight>>;
  limit: Scalars["Int"]["output"];
  skip: Scalars["Int"]["output"];
  total: Scalars["Int"]["output"];
};

export type CategoryHighlightFilter = {
  AND: InputMaybe<Array<InputMaybe<CategoryHighlightFilter>>>;
  OR: InputMaybe<Array<InputMaybe<CategoryHighlightFilter>>>;
  category: InputMaybe<CfCategoryNestedFilter>;
  category_exists: InputMaybe<Scalars["Boolean"]["input"]>;
  contentfulMetadata: InputMaybe<ContentfulMetadataFilter>;
  highlightSlides: InputMaybe<CfHighlightSlideNestedFilter>;
  highlightSlidesCollection_exists: InputMaybe<Scalars["Boolean"]["input"]>;
  rootCategoryName: InputMaybe<Scalars["String"]["input"]>;
  rootCategoryName_contains: InputMaybe<Scalars["String"]["input"]>;
  rootCategoryName_exists: InputMaybe<Scalars["Boolean"]["input"]>;
  rootCategoryName_in: InputMaybe<
    Array<InputMaybe<Scalars["String"]["input"]>>
  >;
  rootCategoryName_not: InputMaybe<Scalars["String"]["input"]>;
  rootCategoryName_not_contains: InputMaybe<Scalars["String"]["input"]>;
  rootCategoryName_not_in: InputMaybe<
    Array<InputMaybe<Scalars["String"]["input"]>>
  >;
  sys: InputMaybe<SysFilter>;
};

export type CategoryHighlightHighlightSlidesCollection = {
  __typename?: "CategoryHighlightHighlightSlidesCollection";
  items: Array<Maybe<HighlightSlide>>;
  limit: Scalars["Int"]["output"];
  skip: Scalars["Int"]["output"];
  total: Scalars["Int"]["output"];
};

export enum CategoryHighlightHighlightSlidesCollectionOrder {
  HrefAsc = "href_ASC",
  HrefDesc = "href_DESC",
  NameAsc = "name_ASC",
  NameDesc = "name_DESC",
  RootCategorySlugAsc = "rootCategorySlug_ASC",
  RootCategorySlugDesc = "rootCategorySlug_DESC",
  ShouldRedirectAsc = "shouldRedirect_ASC",
  ShouldRedirectDesc = "shouldRedirect_DESC",
  SysFirstPublishedAtAsc = "sys_firstPublishedAt_ASC",
  SysFirstPublishedAtDesc = "sys_firstPublishedAt_DESC",
  SysIdAsc = "sys_id_ASC",
  SysIdDesc = "sys_id_DESC",
  SysPublishedAtAsc = "sys_publishedAt_ASC",
  SysPublishedAtDesc = "sys_publishedAt_DESC",
  SysPublishedVersionAsc = "sys_publishedVersion_ASC",
  SysPublishedVersionDesc = "sys_publishedVersion_DESC",
  ThemeAsc = "theme_ASC",
  ThemeDesc = "theme_DESC",
}

export type CategoryHighlightLinkingCollections = {
  __typename?: "CategoryHighlightLinkingCollections";
  entryCollection: Maybe<EntryCollection>;
};

export type CategoryHighlightLinkingCollectionsEntryCollectionArgs = {
  limit?: InputMaybe<Scalars["Int"]["input"]>;
  locale: InputMaybe<Scalars["String"]["input"]>;
  preview: InputMaybe<Scalars["Boolean"]["input"]>;
  skip?: InputMaybe<Scalars["Int"]["input"]>;
};

export enum CategoryHighlightOrder {
  RootCategoryNameAsc = "rootCategoryName_ASC",
  RootCategoryNameDesc = "rootCategoryName_DESC",
  SysFirstPublishedAtAsc = "sys_firstPublishedAt_ASC",
  SysFirstPublishedAtDesc = "sys_firstPublishedAt_DESC",
  SysIdAsc = "sys_id_ASC",
  SysIdDesc = "sys_id_DESC",
  SysPublishedAtAsc = "sys_publishedAt_ASC",
  SysPublishedAtDesc = "sys_publishedAt_DESC",
  SysPublishedVersionAsc = "sys_publishedVersion_ASC",
  SysPublishedVersionDesc = "sys_publishedVersion_DESC",
}

export type CategoryIntersectAttributesCollection = {
  __typename?: "CategoryIntersectAttributesCollection";
  items: Array<Maybe<ProductAttribute>>;
  limit: Scalars["Int"]["output"];
  skip: Scalars["Int"]["output"];
  total: Scalars["Int"]["output"];
};

export enum CategoryIntersectAttributesCollectionOrder {
  NameAsc = "name_ASC",
  NameDesc = "name_DESC",
  SlugAsc = "slug_ASC",
  SlugDesc = "slug_DESC",
  SysFirstPublishedAtAsc = "sys_firstPublishedAt_ASC",
  SysFirstPublishedAtDesc = "sys_firstPublishedAt_DESC",
  SysIdAsc = "sys_id_ASC",
  SysIdDesc = "sys_id_DESC",
  SysPublishedAtAsc = "sys_publishedAt_ASC",
  SysPublishedAtDesc = "sys_publishedAt_DESC",
  SysPublishedVersionAsc = "sys_publishedVersion_ASC",
  SysPublishedVersionDesc = "sys_publishedVersion_DESC",
  TypeAsc = "type_ASC",
  TypeDesc = "type_DESC",
}

export type CategoryLinkingCollections = {
  __typename?: "CategoryLinkingCollections";
  categoriesCollection: Maybe<CategoriesCollection>;
  categoryCollection: Maybe<CategoryCollection>;
  categoryHighlightCollection: Maybe<CategoryHighlightCollection>;
  entryCollection: Maybe<EntryCollection>;
  highlightSlideCollection: Maybe<HighlightSlideCollection>;
};

export type CategoryLinkingCollectionsCategoriesCollectionArgs = {
  limit?: InputMaybe<Scalars["Int"]["input"]>;
  locale: InputMaybe<Scalars["String"]["input"]>;
  order: InputMaybe<
    Array<InputMaybe<CategoryLinkingCollectionsCategoriesCollectionOrder>>
  >;
  preview: InputMaybe<Scalars["Boolean"]["input"]>;
  skip?: InputMaybe<Scalars["Int"]["input"]>;
};

export type CategoryLinkingCollectionsCategoryCollectionArgs = {
  limit?: InputMaybe<Scalars["Int"]["input"]>;
  locale: InputMaybe<Scalars["String"]["input"]>;
  order: InputMaybe<
    Array<InputMaybe<CategoryLinkingCollectionsCategoryCollectionOrder>>
  >;
  preview: InputMaybe<Scalars["Boolean"]["input"]>;
  skip?: InputMaybe<Scalars["Int"]["input"]>;
};

export type CategoryLinkingCollectionsCategoryHighlightCollectionArgs = {
  limit?: InputMaybe<Scalars["Int"]["input"]>;
  locale: InputMaybe<Scalars["String"]["input"]>;
  order: InputMaybe<
    Array<
      InputMaybe<CategoryLinkingCollectionsCategoryHighlightCollectionOrder>
    >
  >;
  preview: InputMaybe<Scalars["Boolean"]["input"]>;
  skip?: InputMaybe<Scalars["Int"]["input"]>;
};

export type CategoryLinkingCollectionsEntryCollectionArgs = {
  limit?: InputMaybe<Scalars["Int"]["input"]>;
  locale: InputMaybe<Scalars["String"]["input"]>;
  preview: InputMaybe<Scalars["Boolean"]["input"]>;
  skip?: InputMaybe<Scalars["Int"]["input"]>;
};

export type CategoryLinkingCollectionsHighlightSlideCollectionArgs = {
  limit?: InputMaybe<Scalars["Int"]["input"]>;
  locale: InputMaybe<Scalars["String"]["input"]>;
  order: InputMaybe<
    Array<InputMaybe<CategoryLinkingCollectionsHighlightSlideCollectionOrder>>
  >;
  preview: InputMaybe<Scalars["Boolean"]["input"]>;
  skip?: InputMaybe<Scalars["Int"]["input"]>;
};

export enum CategoryLinkingCollectionsCategoriesCollectionOrder {
  NameAsc = "name_ASC",
  NameDesc = "name_DESC",
  SysFirstPublishedAtAsc = "sys_firstPublishedAt_ASC",
  SysFirstPublishedAtDesc = "sys_firstPublishedAt_DESC",
  SysIdAsc = "sys_id_ASC",
  SysIdDesc = "sys_id_DESC",
  SysPublishedAtAsc = "sys_publishedAt_ASC",
  SysPublishedAtDesc = "sys_publishedAt_DESC",
  SysPublishedVersionAsc = "sys_publishedVersion_ASC",
  SysPublishedVersionDesc = "sys_publishedVersion_DESC",
}

export enum CategoryLinkingCollectionsCategoryCollectionOrder {
  AutoFillSchemaAsc = "autoFillSchema_ASC",
  AutoFillSchemaDesc = "autoFillSchema_DESC",
  DisplayNameAsc = "displayName_ASC",
  DisplayNameDesc = "displayName_DESC",
  IsRootCategoryAsc = "isRootCategory_ASC",
  IsRootCategoryDesc = "isRootCategory_DESC",
  NameAsc = "name_ASC",
  NameDesc = "name_DESC",
  SlugAsc = "slug_ASC",
  SlugDesc = "slug_DESC",
  SysFirstPublishedAtAsc = "sys_firstPublishedAt_ASC",
  SysFirstPublishedAtDesc = "sys_firstPublishedAt_DESC",
  SysIdAsc = "sys_id_ASC",
  SysIdDesc = "sys_id_DESC",
  SysPublishedAtAsc = "sys_publishedAt_ASC",
  SysPublishedAtDesc = "sys_publishedAt_DESC",
  SysPublishedVersionAsc = "sys_publishedVersion_ASC",
  SysPublishedVersionDesc = "sys_publishedVersion_DESC",
}

export enum CategoryLinkingCollectionsCategoryHighlightCollectionOrder {
  RootCategoryNameAsc = "rootCategoryName_ASC",
  RootCategoryNameDesc = "rootCategoryName_DESC",
  SysFirstPublishedAtAsc = "sys_firstPublishedAt_ASC",
  SysFirstPublishedAtDesc = "sys_firstPublishedAt_DESC",
  SysIdAsc = "sys_id_ASC",
  SysIdDesc = "sys_id_DESC",
  SysPublishedAtAsc = "sys_publishedAt_ASC",
  SysPublishedAtDesc = "sys_publishedAt_DESC",
  SysPublishedVersionAsc = "sys_publishedVersion_ASC",
  SysPublishedVersionDesc = "sys_publishedVersion_DESC",
}

export enum CategoryLinkingCollectionsHighlightSlideCollectionOrder {
  HrefAsc = "href_ASC",
  HrefDesc = "href_DESC",
  NameAsc = "name_ASC",
  NameDesc = "name_DESC",
  RootCategorySlugAsc = "rootCategorySlug_ASC",
  RootCategorySlugDesc = "rootCategorySlug_DESC",
  ShouldRedirectAsc = "shouldRedirect_ASC",
  ShouldRedirectDesc = "shouldRedirect_DESC",
  SysFirstPublishedAtAsc = "sys_firstPublishedAt_ASC",
  SysFirstPublishedAtDesc = "sys_firstPublishedAt_DESC",
  SysIdAsc = "sys_id_ASC",
  SysIdDesc = "sys_id_DESC",
  SysPublishedAtAsc = "sys_publishedAt_ASC",
  SysPublishedAtDesc = "sys_publishedAt_DESC",
  SysPublishedVersionAsc = "sys_publishedVersion_ASC",
  SysPublishedVersionDesc = "sys_publishedVersion_DESC",
  ThemeAsc = "theme_ASC",
  ThemeDesc = "theme_DESC",
}

export enum CategoryOrder {
  AutoFillSchemaAsc = "autoFillSchema_ASC",
  AutoFillSchemaDesc = "autoFillSchema_DESC",
  DisplayNameAsc = "displayName_ASC",
  DisplayNameDesc = "displayName_DESC",
  IsRootCategoryAsc = "isRootCategory_ASC",
  IsRootCategoryDesc = "isRootCategory_DESC",
  NameAsc = "name_ASC",
  NameDesc = "name_DESC",
  SlugAsc = "slug_ASC",
  SlugDesc = "slug_DESC",
  SysFirstPublishedAtAsc = "sys_firstPublishedAt_ASC",
  SysFirstPublishedAtDesc = "sys_firstPublishedAt_DESC",
  SysIdAsc = "sys_id_ASC",
  SysIdDesc = "sys_id_DESC",
  SysPublishedAtAsc = "sys_publishedAt_ASC",
  SysPublishedAtDesc = "sys_publishedAt_DESC",
  SysPublishedVersionAsc = "sys_publishedVersion_ASC",
  SysPublishedVersionDesc = "sys_publishedVersion_DESC",
}

export type CategorySubCategoriesCollection = {
  __typename?: "CategorySubCategoriesCollection";
  items: Array<Maybe<Category>>;
  limit: Scalars["Int"]["output"];
  skip: Scalars["Int"]["output"];
  total: Scalars["Int"]["output"];
};

export enum CategorySubCategoriesCollectionOrder {
  AutoFillSchemaAsc = "autoFillSchema_ASC",
  AutoFillSchemaDesc = "autoFillSchema_DESC",
  DisplayNameAsc = "displayName_ASC",
  DisplayNameDesc = "displayName_DESC",
  IsRootCategoryAsc = "isRootCategory_ASC",
  IsRootCategoryDesc = "isRootCategory_DESC",
  NameAsc = "name_ASC",
  NameDesc = "name_DESC",
  SlugAsc = "slug_ASC",
  SlugDesc = "slug_DESC",
  SysFirstPublishedAtAsc = "sys_firstPublishedAt_ASC",
  SysFirstPublishedAtDesc = "sys_firstPublishedAt_DESC",
  SysIdAsc = "sys_id_ASC",
  SysIdDesc = "sys_id_DESC",
  SysPublishedAtAsc = "sys_publishedAt_ASC",
  SysPublishedAtDesc = "sys_publishedAt_DESC",
  SysPublishedVersionAsc = "sys_publishedVersion_ASC",
  SysPublishedVersionDesc = "sys_publishedVersion_DESC",
}

export type CategoryUnionAttributesCollection = {
  __typename?: "CategoryUnionAttributesCollection";
  items: Array<Maybe<ProductAttribute>>;
  limit: Scalars["Int"]["output"];
  skip: Scalars["Int"]["output"];
  total: Scalars["Int"]["output"];
};

export enum CategoryUnionAttributesCollectionOrder {
  NameAsc = "name_ASC",
  NameDesc = "name_DESC",
  SlugAsc = "slug_ASC",
  SlugDesc = "slug_DESC",
  SysFirstPublishedAtAsc = "sys_firstPublishedAt_ASC",
  SysFirstPublishedAtDesc = "sys_firstPublishedAt_DESC",
  SysIdAsc = "sys_id_ASC",
  SysIdDesc = "sys_id_DESC",
  SysPublishedAtAsc = "sys_publishedAt_ASC",
  SysPublishedAtDesc = "sys_publishedAt_DESC",
  SysPublishedVersionAsc = "sys_publishedVersion_ASC",
  SysPublishedVersionDesc = "sys_publishedVersion_DESC",
  TypeAsc = "type_ASC",
  TypeDesc = "type_DESC",
}

export type ContentfulMetadata = {
  __typename?: "ContentfulMetadata";
  tags: Array<Maybe<ContentfulTag>>;
};

export type ContentfulMetadataFilter = {
  tags: InputMaybe<ContentfulMetadataTagsFilter>;
  tags_exists: InputMaybe<Scalars["Boolean"]["input"]>;
};

export type ContentfulMetadataTagsFilter = {
  id_contains_all: InputMaybe<Array<InputMaybe<Scalars["String"]["input"]>>>;
  id_contains_none: InputMaybe<Array<InputMaybe<Scalars["String"]["input"]>>>;
  id_contains_some: InputMaybe<Array<InputMaybe<Scalars["String"]["input"]>>>;
};

/**
 * Represents a tag entity for finding and organizing content easily.
 *     Find out more here: https://www.contentful.com/developers/docs/references/content-delivery-api/#/reference/content-tags
 */
export type ContentfulTag = {
  __typename?: "ContentfulTag";
  id: Maybe<Scalars["String"]["output"]>;
  name: Maybe<Scalars["String"]["output"]>;
};

export type Entry = {
  contentfulMetadata: ContentfulMetadata;
  sys: Sys;
};

export type EntryCollection = {
  __typename?: "EntryCollection";
  items: Array<Maybe<Entry>>;
  limit: Scalars["Int"]["output"];
  skip: Scalars["Int"]["output"];
  total: Scalars["Int"]["output"];
};

export type EntryFilter = {
  AND: InputMaybe<Array<InputMaybe<EntryFilter>>>;
  OR: InputMaybe<Array<InputMaybe<EntryFilter>>>;
  contentfulMetadata: InputMaybe<ContentfulMetadataFilter>;
  sys: InputMaybe<SysFilter>;
};

export enum EntryOrder {
  SysFirstPublishedAtAsc = "sys_firstPublishedAt_ASC",
  SysFirstPublishedAtDesc = "sys_firstPublishedAt_DESC",
  SysIdAsc = "sys_id_ASC",
  SysIdDesc = "sys_id_DESC",
  SysPublishedAtAsc = "sys_publishedAt_ASC",
  SysPublishedAtDesc = "sys_publishedAt_DESC",
  SysPublishedVersionAsc = "sys_publishedVersion_ASC",
  SysPublishedVersionDesc = "sys_publishedVersion_DESC",
}

/** [See type definition](https://app.contentful.com/spaces/nh559twm3d3o/content_types/highlightSlide) */
export type HighlightSlide = Entry & {
  __typename?: "HighlightSlide";
  category: Maybe<Category>;
  contentfulMetadata: ContentfulMetadata;
  href: Maybe<Scalars["String"]["output"]>;
  linkedFrom: Maybe<HighlightSlideLinkingCollections>;
  media: Maybe<Asset>;
  name: Maybe<Scalars["String"]["output"]>;
  rootCategorySlug: Maybe<Scalars["String"]["output"]>;
  shouldRedirect: Maybe<Scalars["Boolean"]["output"]>;
  sys: Sys;
  theme: Maybe<Scalars["String"]["output"]>;
};

/** [See type definition](https://app.contentful.com/spaces/nh559twm3d3o/content_types/highlightSlide) */
export type HighlightSlideCategoryArgs = {
  locale: InputMaybe<Scalars["String"]["input"]>;
  preview: InputMaybe<Scalars["Boolean"]["input"]>;
  where: InputMaybe<CategoryFilter>;
};

/** [See type definition](https://app.contentful.com/spaces/nh559twm3d3o/content_types/highlightSlide) */
export type HighlightSlideHrefArgs = {
  locale: InputMaybe<Scalars["String"]["input"]>;
};

/** [See type definition](https://app.contentful.com/spaces/nh559twm3d3o/content_types/highlightSlide) */
export type HighlightSlideLinkedFromArgs = {
  allowedLocales: InputMaybe<Array<InputMaybe<Scalars["String"]["input"]>>>;
};

/** [See type definition](https://app.contentful.com/spaces/nh559twm3d3o/content_types/highlightSlide) */
export type HighlightSlideMediaArgs = {
  locale: InputMaybe<Scalars["String"]["input"]>;
  preview: InputMaybe<Scalars["Boolean"]["input"]>;
};

/** [See type definition](https://app.contentful.com/spaces/nh559twm3d3o/content_types/highlightSlide) */
export type HighlightSlideNameArgs = {
  locale: InputMaybe<Scalars["String"]["input"]>;
};

/** [See type definition](https://app.contentful.com/spaces/nh559twm3d3o/content_types/highlightSlide) */
export type HighlightSlideRootCategorySlugArgs = {
  locale: InputMaybe<Scalars["String"]["input"]>;
};

/** [See type definition](https://app.contentful.com/spaces/nh559twm3d3o/content_types/highlightSlide) */
export type HighlightSlideShouldRedirectArgs = {
  locale: InputMaybe<Scalars["String"]["input"]>;
};

/** [See type definition](https://app.contentful.com/spaces/nh559twm3d3o/content_types/highlightSlide) */
export type HighlightSlideThemeArgs = {
  locale: InputMaybe<Scalars["String"]["input"]>;
};

export type HighlightSlideCollection = {
  __typename?: "HighlightSlideCollection";
  items: Array<Maybe<HighlightSlide>>;
  limit: Scalars["Int"]["output"];
  skip: Scalars["Int"]["output"];
  total: Scalars["Int"]["output"];
};

export type HighlightSlideFilter = {
  AND: InputMaybe<Array<InputMaybe<HighlightSlideFilter>>>;
  OR: InputMaybe<Array<InputMaybe<HighlightSlideFilter>>>;
  category: InputMaybe<CfCategoryNestedFilter>;
  category_exists: InputMaybe<Scalars["Boolean"]["input"]>;
  contentfulMetadata: InputMaybe<ContentfulMetadataFilter>;
  href: InputMaybe<Scalars["String"]["input"]>;
  href_contains: InputMaybe<Scalars["String"]["input"]>;
  href_exists: InputMaybe<Scalars["Boolean"]["input"]>;
  href_in: InputMaybe<Array<InputMaybe<Scalars["String"]["input"]>>>;
  href_not: InputMaybe<Scalars["String"]["input"]>;
  href_not_contains: InputMaybe<Scalars["String"]["input"]>;
  href_not_in: InputMaybe<Array<InputMaybe<Scalars["String"]["input"]>>>;
  media_exists: InputMaybe<Scalars["Boolean"]["input"]>;
  name: InputMaybe<Scalars["String"]["input"]>;
  name_contains: InputMaybe<Scalars["String"]["input"]>;
  name_exists: InputMaybe<Scalars["Boolean"]["input"]>;
  name_in: InputMaybe<Array<InputMaybe<Scalars["String"]["input"]>>>;
  name_not: InputMaybe<Scalars["String"]["input"]>;
  name_not_contains: InputMaybe<Scalars["String"]["input"]>;
  name_not_in: InputMaybe<Array<InputMaybe<Scalars["String"]["input"]>>>;
  rootCategorySlug: InputMaybe<Scalars["String"]["input"]>;
  rootCategorySlug_contains: InputMaybe<Scalars["String"]["input"]>;
  rootCategorySlug_exists: InputMaybe<Scalars["Boolean"]["input"]>;
  rootCategorySlug_in: InputMaybe<
    Array<InputMaybe<Scalars["String"]["input"]>>
  >;
  rootCategorySlug_not: InputMaybe<Scalars["String"]["input"]>;
  rootCategorySlug_not_contains: InputMaybe<Scalars["String"]["input"]>;
  rootCategorySlug_not_in: InputMaybe<
    Array<InputMaybe<Scalars["String"]["input"]>>
  >;
  shouldRedirect: InputMaybe<Scalars["Boolean"]["input"]>;
  shouldRedirect_exists: InputMaybe<Scalars["Boolean"]["input"]>;
  shouldRedirect_not: InputMaybe<Scalars["Boolean"]["input"]>;
  sys: InputMaybe<SysFilter>;
  theme: InputMaybe<Scalars["String"]["input"]>;
  theme_contains: InputMaybe<Scalars["String"]["input"]>;
  theme_exists: InputMaybe<Scalars["Boolean"]["input"]>;
  theme_in: InputMaybe<Array<InputMaybe<Scalars["String"]["input"]>>>;
  theme_not: InputMaybe<Scalars["String"]["input"]>;
  theme_not_contains: InputMaybe<Scalars["String"]["input"]>;
  theme_not_in: InputMaybe<Array<InputMaybe<Scalars["String"]["input"]>>>;
};

export type HighlightSlideLinkingCollections = {
  __typename?: "HighlightSlideLinkingCollections";
  categoryHighlightCollection: Maybe<CategoryHighlightCollection>;
  entryCollection: Maybe<EntryCollection>;
};

export type HighlightSlideLinkingCollectionsCategoryHighlightCollectionArgs = {
  limit?: InputMaybe<Scalars["Int"]["input"]>;
  locale: InputMaybe<Scalars["String"]["input"]>;
  order: InputMaybe<
    Array<
      InputMaybe<HighlightSlideLinkingCollectionsCategoryHighlightCollectionOrder>
    >
  >;
  preview: InputMaybe<Scalars["Boolean"]["input"]>;
  skip?: InputMaybe<Scalars["Int"]["input"]>;
};

export type HighlightSlideLinkingCollectionsEntryCollectionArgs = {
  limit?: InputMaybe<Scalars["Int"]["input"]>;
  locale: InputMaybe<Scalars["String"]["input"]>;
  preview: InputMaybe<Scalars["Boolean"]["input"]>;
  skip?: InputMaybe<Scalars["Int"]["input"]>;
};

export enum HighlightSlideLinkingCollectionsCategoryHighlightCollectionOrder {
  RootCategoryNameAsc = "rootCategoryName_ASC",
  RootCategoryNameDesc = "rootCategoryName_DESC",
  SysFirstPublishedAtAsc = "sys_firstPublishedAt_ASC",
  SysFirstPublishedAtDesc = "sys_firstPublishedAt_DESC",
  SysIdAsc = "sys_id_ASC",
  SysIdDesc = "sys_id_DESC",
  SysPublishedAtAsc = "sys_publishedAt_ASC",
  SysPublishedAtDesc = "sys_publishedAt_DESC",
  SysPublishedVersionAsc = "sys_publishedVersion_ASC",
  SysPublishedVersionDesc = "sys_publishedVersion_DESC",
}

export enum HighlightSlideOrder {
  HrefAsc = "href_ASC",
  HrefDesc = "href_DESC",
  NameAsc = "name_ASC",
  NameDesc = "name_DESC",
  RootCategorySlugAsc = "rootCategorySlug_ASC",
  RootCategorySlugDesc = "rootCategorySlug_DESC",
  ShouldRedirectAsc = "shouldRedirect_ASC",
  ShouldRedirectDesc = "shouldRedirect_DESC",
  SysFirstPublishedAtAsc = "sys_firstPublishedAt_ASC",
  SysFirstPublishedAtDesc = "sys_firstPublishedAt_DESC",
  SysIdAsc = "sys_id_ASC",
  SysIdDesc = "sys_id_DESC",
  SysPublishedAtAsc = "sys_publishedAt_ASC",
  SysPublishedAtDesc = "sys_publishedAt_DESC",
  SysPublishedVersionAsc = "sys_publishedVersion_ASC",
  SysPublishedVersionDesc = "sys_publishedVersion_DESC",
  ThemeAsc = "theme_ASC",
  ThemeDesc = "theme_DESC",
}

export enum ImageFormat {
  Avif = "AVIF",
  /** JPG image format. */
  Jpg = "JPG",
  /**
   * Progressive JPG format stores multiple passes of an image in progressively higher detail.
   *         When a progressive image is loading, the viewer will first see a lower quality pixelated version which
   *         will gradually improve in detail, until the image is fully downloaded. This is to display an image as
   *         early as possible to make the layout look as designed.
   */
  JpgProgressive = "JPG_PROGRESSIVE",
  /** PNG image format */
  Png = "PNG",
  /**
   * 8-bit PNG images support up to 256 colors and weigh less than the standard 24-bit PNG equivalent.
   *         The 8-bit PNG format is mostly used for simple images, such as icons or logos.
   */
  Png8 = "PNG8",
  /** WebP image format. */
  Webp = "WEBP",
}

export enum ImageResizeFocus {
  /** Focus the resizing on the bottom. */
  Bottom = "BOTTOM",
  /** Focus the resizing on the bottom left. */
  BottomLeft = "BOTTOM_LEFT",
  /** Focus the resizing on the bottom right. */
  BottomRight = "BOTTOM_RIGHT",
  /** Focus the resizing on the center. */
  Center = "CENTER",
  /** Focus the resizing on the largest face. */
  Face = "FACE",
  /** Focus the resizing on the area containing all the faces. */
  Faces = "FACES",
  /** Focus the resizing on the left. */
  Left = "LEFT",
  /** Focus the resizing on the right. */
  Right = "RIGHT",
  /** Focus the resizing on the top. */
  Top = "TOP",
  /** Focus the resizing on the top left. */
  TopLeft = "TOP_LEFT",
  /** Focus the resizing on the top right. */
  TopRight = "TOP_RIGHT",
}

export enum ImageResizeStrategy {
  /** Crops a part of the original image to fit into the specified dimensions. */
  Crop = "CROP",
  /** Resizes the image to the specified dimensions, cropping the image if needed. */
  Fill = "FILL",
  /** Resizes the image to fit into the specified dimensions. */
  Fit = "FIT",
  /**
   * Resizes the image to the specified dimensions, padding the image if needed.
   *         Uses desired background color as padding color.
   */
  Pad = "PAD",
  /** Resizes the image to the specified dimensions, changing the original aspect ratio if needed. */
  Scale = "SCALE",
  /** Creates a thumbnail from the image. */
  Thumb = "THUMB",
}

export type ImageTransformOptions = {
  /**
   * Desired background color, used with corner radius or `PAD` resize strategy.
   *         Defaults to transparent (for `PNG`, `PNG8` and `WEBP`) or white (for `JPG` and `JPG_PROGRESSIVE`).
   */
  backgroundColor: InputMaybe<Scalars["HexColor"]["input"]>;
  /**
   * Desired corner radius in pixels.
   *         Results in an image with rounded corners (pass `-1` for a full circle/ellipse).
   *         Defaults to `0`. Uses desired background color as padding color,
   *         unless the format is `JPG` or `JPG_PROGRESSIVE` and resize strategy is `PAD`, then defaults to white.
   */
  cornerRadius: InputMaybe<Scalars["Int"]["input"]>;
  /** Desired image format. Defaults to the original image format. */
  format: InputMaybe<ImageFormat>;
  /** Desired height in pixels. Defaults to the original image height. */
  height: InputMaybe<Scalars["Dimension"]["input"]>;
  /**
   * Desired quality of the image in percents.
   *         Used for `PNG8`, `JPG`, `JPG_PROGRESSIVE` and `WEBP` formats.
   */
  quality: InputMaybe<Scalars["Quality"]["input"]>;
  /** Desired resize focus area. Defaults to `CENTER`. */
  resizeFocus: InputMaybe<ImageResizeFocus>;
  /** Desired resize strategy. Defaults to `FIT`. */
  resizeStrategy: InputMaybe<ImageResizeStrategy>;
  /** Desired width in pixels. Defaults to the original image width. */
  width: InputMaybe<Scalars["Dimension"]["input"]>;
};

/** [See type definition](https://app.contentful.com/spaces/nh559twm3d3o/content_types/product) */
export type Product = Entry & {
  __typename?: "Product";
  contentfulMetadata: ContentfulMetadata;
  description: Maybe<Scalars["String"]["output"]>;
  linkedFrom: Maybe<ProductLinkingCollections>;
  name: Maybe<Scalars["String"]["output"]>;
  slug: Maybe<Scalars["String"]["output"]>;
  sys: Sys;
  variantsCollection: Maybe<ProductVariantsCollection>;
};

/** [See type definition](https://app.contentful.com/spaces/nh559twm3d3o/content_types/product) */
export type ProductDescriptionArgs = {
  locale: InputMaybe<Scalars["String"]["input"]>;
};

/** [See type definition](https://app.contentful.com/spaces/nh559twm3d3o/content_types/product) */
export type ProductLinkedFromArgs = {
  allowedLocales: InputMaybe<Array<InputMaybe<Scalars["String"]["input"]>>>;
};

/** [See type definition](https://app.contentful.com/spaces/nh559twm3d3o/content_types/product) */
export type ProductNameArgs = {
  locale: InputMaybe<Scalars["String"]["input"]>;
};

/** [See type definition](https://app.contentful.com/spaces/nh559twm3d3o/content_types/product) */
export type ProductSlugArgs = {
  locale: InputMaybe<Scalars["String"]["input"]>;
};

/** [See type definition](https://app.contentful.com/spaces/nh559twm3d3o/content_types/product) */
export type ProductVariantsCollectionArgs = {
  limit?: InputMaybe<Scalars["Int"]["input"]>;
  locale: InputMaybe<Scalars["String"]["input"]>;
  order: InputMaybe<Array<InputMaybe<ProductVariantsCollectionOrder>>>;
  preview: InputMaybe<Scalars["Boolean"]["input"]>;
  skip?: InputMaybe<Scalars["Int"]["input"]>;
  where: InputMaybe<ProductVariantFilter>;
};

/** [See type definition](https://app.contentful.com/spaces/nh559twm3d3o/content_types/productAttribute) */
export type ProductAttribute = Entry & {
  __typename?: "ProductAttribute";
  contentfulMetadata: ContentfulMetadata;
  linkedFrom: Maybe<ProductAttributeLinkingCollections>;
  name: Maybe<Scalars["String"]["output"]>;
  slug: Maybe<Scalars["String"]["output"]>;
  sys: Sys;
  type: Maybe<Scalars["String"]["output"]>;
  valuesCollection: Maybe<ProductAttributeValuesCollection>;
};

/** [See type definition](https://app.contentful.com/spaces/nh559twm3d3o/content_types/productAttribute) */
export type ProductAttributeLinkedFromArgs = {
  allowedLocales: InputMaybe<Array<InputMaybe<Scalars["String"]["input"]>>>;
};

/** [See type definition](https://app.contentful.com/spaces/nh559twm3d3o/content_types/productAttribute) */
export type ProductAttributeNameArgs = {
  locale: InputMaybe<Scalars["String"]["input"]>;
};

/** [See type definition](https://app.contentful.com/spaces/nh559twm3d3o/content_types/productAttribute) */
export type ProductAttributeSlugArgs = {
  locale: InputMaybe<Scalars["String"]["input"]>;
};

/** [See type definition](https://app.contentful.com/spaces/nh559twm3d3o/content_types/productAttribute) */
export type ProductAttributeTypeArgs = {
  locale: InputMaybe<Scalars["String"]["input"]>;
};

/** [See type definition](https://app.contentful.com/spaces/nh559twm3d3o/content_types/productAttribute) */
export type ProductAttributeValuesCollectionArgs = {
  limit?: InputMaybe<Scalars["Int"]["input"]>;
  locale: InputMaybe<Scalars["String"]["input"]>;
  order: InputMaybe<Array<InputMaybe<ProductAttributeValuesCollectionOrder>>>;
  preview: InputMaybe<Scalars["Boolean"]["input"]>;
  skip?: InputMaybe<Scalars["Int"]["input"]>;
  where: InputMaybe<ProductAttributeFilter>;
};

export type ProductAttributeCollection = {
  __typename?: "ProductAttributeCollection";
  items: Array<Maybe<ProductAttribute>>;
  limit: Scalars["Int"]["output"];
  skip: Scalars["Int"]["output"];
  total: Scalars["Int"]["output"];
};

export type ProductAttributeFilter = {
  AND: InputMaybe<Array<InputMaybe<ProductAttributeFilter>>>;
  OR: InputMaybe<Array<InputMaybe<ProductAttributeFilter>>>;
  contentfulMetadata: InputMaybe<ContentfulMetadataFilter>;
  name: InputMaybe<Scalars["String"]["input"]>;
  name_contains: InputMaybe<Scalars["String"]["input"]>;
  name_exists: InputMaybe<Scalars["Boolean"]["input"]>;
  name_in: InputMaybe<Array<InputMaybe<Scalars["String"]["input"]>>>;
  name_not: InputMaybe<Scalars["String"]["input"]>;
  name_not_contains: InputMaybe<Scalars["String"]["input"]>;
  name_not_in: InputMaybe<Array<InputMaybe<Scalars["String"]["input"]>>>;
  slug: InputMaybe<Scalars["String"]["input"]>;
  slug_contains: InputMaybe<Scalars["String"]["input"]>;
  slug_exists: InputMaybe<Scalars["Boolean"]["input"]>;
  slug_in: InputMaybe<Array<InputMaybe<Scalars["String"]["input"]>>>;
  slug_not: InputMaybe<Scalars["String"]["input"]>;
  slug_not_contains: InputMaybe<Scalars["String"]["input"]>;
  slug_not_in: InputMaybe<Array<InputMaybe<Scalars["String"]["input"]>>>;
  sys: InputMaybe<SysFilter>;
  type: InputMaybe<Scalars["String"]["input"]>;
  type_contains: InputMaybe<Scalars["String"]["input"]>;
  type_exists: InputMaybe<Scalars["Boolean"]["input"]>;
  type_in: InputMaybe<Array<InputMaybe<Scalars["String"]["input"]>>>;
  type_not: InputMaybe<Scalars["String"]["input"]>;
  type_not_contains: InputMaybe<Scalars["String"]["input"]>;
  type_not_in: InputMaybe<Array<InputMaybe<Scalars["String"]["input"]>>>;
  values: InputMaybe<CfProductAttributeNestedFilter>;
  valuesCollection_exists: InputMaybe<Scalars["Boolean"]["input"]>;
};

export type ProductAttributeLinkingCollections = {
  __typename?: "ProductAttributeLinkingCollections";
  categoryCollection: Maybe<CategoryCollection>;
  entryCollection: Maybe<EntryCollection>;
  productAttributeCollection: Maybe<ProductAttributeCollection>;
  productVariantCollection: Maybe<ProductVariantCollection>;
};

export type ProductAttributeLinkingCollectionsCategoryCollectionArgs = {
  limit?: InputMaybe<Scalars["Int"]["input"]>;
  locale: InputMaybe<Scalars["String"]["input"]>;
  order: InputMaybe<
    Array<InputMaybe<ProductAttributeLinkingCollectionsCategoryCollectionOrder>>
  >;
  preview: InputMaybe<Scalars["Boolean"]["input"]>;
  skip?: InputMaybe<Scalars["Int"]["input"]>;
};

export type ProductAttributeLinkingCollectionsEntryCollectionArgs = {
  limit?: InputMaybe<Scalars["Int"]["input"]>;
  locale: InputMaybe<Scalars["String"]["input"]>;
  preview: InputMaybe<Scalars["Boolean"]["input"]>;
  skip?: InputMaybe<Scalars["Int"]["input"]>;
};

export type ProductAttributeLinkingCollectionsProductAttributeCollectionArgs = {
  limit?: InputMaybe<Scalars["Int"]["input"]>;
  locale: InputMaybe<Scalars["String"]["input"]>;
  order: InputMaybe<
    Array<
      InputMaybe<ProductAttributeLinkingCollectionsProductAttributeCollectionOrder>
    >
  >;
  preview: InputMaybe<Scalars["Boolean"]["input"]>;
  skip?: InputMaybe<Scalars["Int"]["input"]>;
};

export type ProductAttributeLinkingCollectionsProductVariantCollectionArgs = {
  limit?: InputMaybe<Scalars["Int"]["input"]>;
  locale: InputMaybe<Scalars["String"]["input"]>;
  order: InputMaybe<
    Array<
      InputMaybe<ProductAttributeLinkingCollectionsProductVariantCollectionOrder>
    >
  >;
  preview: InputMaybe<Scalars["Boolean"]["input"]>;
  skip?: InputMaybe<Scalars["Int"]["input"]>;
};

export enum ProductAttributeLinkingCollectionsCategoryCollectionOrder {
  AutoFillSchemaAsc = "autoFillSchema_ASC",
  AutoFillSchemaDesc = "autoFillSchema_DESC",
  DisplayNameAsc = "displayName_ASC",
  DisplayNameDesc = "displayName_DESC",
  IsRootCategoryAsc = "isRootCategory_ASC",
  IsRootCategoryDesc = "isRootCategory_DESC",
  NameAsc = "name_ASC",
  NameDesc = "name_DESC",
  SlugAsc = "slug_ASC",
  SlugDesc = "slug_DESC",
  SysFirstPublishedAtAsc = "sys_firstPublishedAt_ASC",
  SysFirstPublishedAtDesc = "sys_firstPublishedAt_DESC",
  SysIdAsc = "sys_id_ASC",
  SysIdDesc = "sys_id_DESC",
  SysPublishedAtAsc = "sys_publishedAt_ASC",
  SysPublishedAtDesc = "sys_publishedAt_DESC",
  SysPublishedVersionAsc = "sys_publishedVersion_ASC",
  SysPublishedVersionDesc = "sys_publishedVersion_DESC",
}

export enum ProductAttributeLinkingCollectionsProductAttributeCollectionOrder {
  NameAsc = "name_ASC",
  NameDesc = "name_DESC",
  SlugAsc = "slug_ASC",
  SlugDesc = "slug_DESC",
  SysFirstPublishedAtAsc = "sys_firstPublishedAt_ASC",
  SysFirstPublishedAtDesc = "sys_firstPublishedAt_DESC",
  SysIdAsc = "sys_id_ASC",
  SysIdDesc = "sys_id_DESC",
  SysPublishedAtAsc = "sys_publishedAt_ASC",
  SysPublishedAtDesc = "sys_publishedAt_DESC",
  SysPublishedVersionAsc = "sys_publishedVersion_ASC",
  SysPublishedVersionDesc = "sys_publishedVersion_DESC",
  TypeAsc = "type_ASC",
  TypeDesc = "type_DESC",
}

export enum ProductAttributeLinkingCollectionsProductVariantCollectionOrder {
  ColorCodeAsc = "colorCode_ASC",
  ColorCodeDesc = "colorCode_DESC",
  ColorNameAsc = "colorName_ASC",
  ColorNameDesc = "colorName_DESC",
  FirstMediaInOverviewAsc = "firstMediaInOverview_ASC",
  FirstMediaInOverviewDesc = "firstMediaInOverview_DESC",
  PriceAsc = "price_ASC",
  PriceDesc = "price_DESC",
  RefAsc = "ref_ASC",
  RefDesc = "ref_DESC",
  SysFirstPublishedAtAsc = "sys_firstPublishedAt_ASC",
  SysFirstPublishedAtDesc = "sys_firstPublishedAt_DESC",
  SysIdAsc = "sys_id_ASC",
  SysIdDesc = "sys_id_DESC",
  SysPublishedAtAsc = "sys_publishedAt_ASC",
  SysPublishedAtDesc = "sys_publishedAt_DESC",
  SysPublishedVersionAsc = "sys_publishedVersion_ASC",
  SysPublishedVersionDesc = "sys_publishedVersion_DESC",
}

export enum ProductAttributeOrder {
  NameAsc = "name_ASC",
  NameDesc = "name_DESC",
  SlugAsc = "slug_ASC",
  SlugDesc = "slug_DESC",
  SysFirstPublishedAtAsc = "sys_firstPublishedAt_ASC",
  SysFirstPublishedAtDesc = "sys_firstPublishedAt_DESC",
  SysIdAsc = "sys_id_ASC",
  SysIdDesc = "sys_id_DESC",
  SysPublishedAtAsc = "sys_publishedAt_ASC",
  SysPublishedAtDesc = "sys_publishedAt_DESC",
  SysPublishedVersionAsc = "sys_publishedVersion_ASC",
  SysPublishedVersionDesc = "sys_publishedVersion_DESC",
  TypeAsc = "type_ASC",
  TypeDesc = "type_DESC",
}

export type ProductAttributeValuesCollection = {
  __typename?: "ProductAttributeValuesCollection";
  items: Array<Maybe<ProductAttribute>>;
  limit: Scalars["Int"]["output"];
  skip: Scalars["Int"]["output"];
  total: Scalars["Int"]["output"];
};

export enum ProductAttributeValuesCollectionOrder {
  NameAsc = "name_ASC",
  NameDesc = "name_DESC",
  SlugAsc = "slug_ASC",
  SlugDesc = "slug_DESC",
  SysFirstPublishedAtAsc = "sys_firstPublishedAt_ASC",
  SysFirstPublishedAtDesc = "sys_firstPublishedAt_DESC",
  SysIdAsc = "sys_id_ASC",
  SysIdDesc = "sys_id_DESC",
  SysPublishedAtAsc = "sys_publishedAt_ASC",
  SysPublishedAtDesc = "sys_publishedAt_DESC",
  SysPublishedVersionAsc = "sys_publishedVersion_ASC",
  SysPublishedVersionDesc = "sys_publishedVersion_DESC",
  TypeAsc = "type_ASC",
  TypeDesc = "type_DESC",
}

export type ProductCollection = {
  __typename?: "ProductCollection";
  items: Array<Maybe<Product>>;
  limit: Scalars["Int"]["output"];
  skip: Scalars["Int"]["output"];
  total: Scalars["Int"]["output"];
};

export type ProductFilter = {
  AND: InputMaybe<Array<InputMaybe<ProductFilter>>>;
  OR: InputMaybe<Array<InputMaybe<ProductFilter>>>;
  contentfulMetadata: InputMaybe<ContentfulMetadataFilter>;
  description: InputMaybe<Scalars["String"]["input"]>;
  description_contains: InputMaybe<Scalars["String"]["input"]>;
  description_exists: InputMaybe<Scalars["Boolean"]["input"]>;
  description_in: InputMaybe<Array<InputMaybe<Scalars["String"]["input"]>>>;
  description_not: InputMaybe<Scalars["String"]["input"]>;
  description_not_contains: InputMaybe<Scalars["String"]["input"]>;
  description_not_in: InputMaybe<Array<InputMaybe<Scalars["String"]["input"]>>>;
  name: InputMaybe<Scalars["String"]["input"]>;
  name_contains: InputMaybe<Scalars["String"]["input"]>;
  name_exists: InputMaybe<Scalars["Boolean"]["input"]>;
  name_in: InputMaybe<Array<InputMaybe<Scalars["String"]["input"]>>>;
  name_not: InputMaybe<Scalars["String"]["input"]>;
  name_not_contains: InputMaybe<Scalars["String"]["input"]>;
  name_not_in: InputMaybe<Array<InputMaybe<Scalars["String"]["input"]>>>;
  slug: InputMaybe<Scalars["String"]["input"]>;
  slug_contains: InputMaybe<Scalars["String"]["input"]>;
  slug_exists: InputMaybe<Scalars["Boolean"]["input"]>;
  slug_in: InputMaybe<Array<InputMaybe<Scalars["String"]["input"]>>>;
  slug_not: InputMaybe<Scalars["String"]["input"]>;
  slug_not_contains: InputMaybe<Scalars["String"]["input"]>;
  slug_not_in: InputMaybe<Array<InputMaybe<Scalars["String"]["input"]>>>;
  sys: InputMaybe<SysFilter>;
  variants: InputMaybe<CfProductVariantNestedFilter>;
  variantsCollection_exists: InputMaybe<Scalars["Boolean"]["input"]>;
};

/** [See type definition](https://app.contentful.com/spaces/nh559twm3d3o/content_types/productGroup) */
export type ProductGroup = Entry & {
  __typename?: "ProductGroup";
  contentfulMetadata: ContentfulMetadata;
  firstMediaOfEachVariant: Maybe<Array<Maybe<Scalars["String"]["output"]>>>;
  highlightMedia: Maybe<Asset>;
  linkedFrom: Maybe<ProductGroupLinkingCollections>;
  productVariantsCollection: Maybe<ProductGroupProductVariantsCollection>;
  sys: Sys;
  type: Maybe<Scalars["String"]["output"]>;
};

/** [See type definition](https://app.contentful.com/spaces/nh559twm3d3o/content_types/productGroup) */
export type ProductGroupFirstMediaOfEachVariantArgs = {
  locale: InputMaybe<Scalars["String"]["input"]>;
};

/** [See type definition](https://app.contentful.com/spaces/nh559twm3d3o/content_types/productGroup) */
export type ProductGroupHighlightMediaArgs = {
  locale: InputMaybe<Scalars["String"]["input"]>;
  preview: InputMaybe<Scalars["Boolean"]["input"]>;
};

/** [See type definition](https://app.contentful.com/spaces/nh559twm3d3o/content_types/productGroup) */
export type ProductGroupLinkedFromArgs = {
  allowedLocales: InputMaybe<Array<InputMaybe<Scalars["String"]["input"]>>>;
};

/** [See type definition](https://app.contentful.com/spaces/nh559twm3d3o/content_types/productGroup) */
export type ProductGroupProductVariantsCollectionArgs = {
  limit?: InputMaybe<Scalars["Int"]["input"]>;
  locale: InputMaybe<Scalars["String"]["input"]>;
  order: InputMaybe<
    Array<InputMaybe<ProductGroupProductVariantsCollectionOrder>>
  >;
  preview: InputMaybe<Scalars["Boolean"]["input"]>;
  skip?: InputMaybe<Scalars["Int"]["input"]>;
  where: InputMaybe<ProductVariantFilter>;
};

/** [See type definition](https://app.contentful.com/spaces/nh559twm3d3o/content_types/productGroup) */
export type ProductGroupTypeArgs = {
  locale: InputMaybe<Scalars["String"]["input"]>;
};

export type ProductGroupCollection = {
  __typename?: "ProductGroupCollection";
  items: Array<Maybe<ProductGroup>>;
  limit: Scalars["Int"]["output"];
  skip: Scalars["Int"]["output"];
  total: Scalars["Int"]["output"];
};

export type ProductGroupFilter = {
  AND: InputMaybe<Array<InputMaybe<ProductGroupFilter>>>;
  OR: InputMaybe<Array<InputMaybe<ProductGroupFilter>>>;
  contentfulMetadata: InputMaybe<ContentfulMetadataFilter>;
  firstMediaOfEachVariant_contains_all: InputMaybe<
    Array<InputMaybe<Scalars["String"]["input"]>>
  >;
  firstMediaOfEachVariant_contains_none: InputMaybe<
    Array<InputMaybe<Scalars["String"]["input"]>>
  >;
  firstMediaOfEachVariant_contains_some: InputMaybe<
    Array<InputMaybe<Scalars["String"]["input"]>>
  >;
  firstMediaOfEachVariant_exists: InputMaybe<Scalars["Boolean"]["input"]>;
  highlightMedia_exists: InputMaybe<Scalars["Boolean"]["input"]>;
  productVariants: InputMaybe<CfProductVariantNestedFilter>;
  productVariantsCollection_exists: InputMaybe<Scalars["Boolean"]["input"]>;
  sys: InputMaybe<SysFilter>;
  type: InputMaybe<Scalars["String"]["input"]>;
  type_contains: InputMaybe<Scalars["String"]["input"]>;
  type_exists: InputMaybe<Scalars["Boolean"]["input"]>;
  type_in: InputMaybe<Array<InputMaybe<Scalars["String"]["input"]>>>;
  type_not: InputMaybe<Scalars["String"]["input"]>;
  type_not_contains: InputMaybe<Scalars["String"]["input"]>;
  type_not_in: InputMaybe<Array<InputMaybe<Scalars["String"]["input"]>>>;
};

export type ProductGroupLinkingCollections = {
  __typename?: "ProductGroupLinkingCollections";
  categoryCollection: Maybe<CategoryCollection>;
  entryCollection: Maybe<EntryCollection>;
};

export type ProductGroupLinkingCollectionsCategoryCollectionArgs = {
  limit?: InputMaybe<Scalars["Int"]["input"]>;
  locale: InputMaybe<Scalars["String"]["input"]>;
  order: InputMaybe<
    Array<InputMaybe<ProductGroupLinkingCollectionsCategoryCollectionOrder>>
  >;
  preview: InputMaybe<Scalars["Boolean"]["input"]>;
  skip?: InputMaybe<Scalars["Int"]["input"]>;
};

export type ProductGroupLinkingCollectionsEntryCollectionArgs = {
  limit?: InputMaybe<Scalars["Int"]["input"]>;
  locale: InputMaybe<Scalars["String"]["input"]>;
  preview: InputMaybe<Scalars["Boolean"]["input"]>;
  skip?: InputMaybe<Scalars["Int"]["input"]>;
};

export enum ProductGroupLinkingCollectionsCategoryCollectionOrder {
  AutoFillSchemaAsc = "autoFillSchema_ASC",
  AutoFillSchemaDesc = "autoFillSchema_DESC",
  DisplayNameAsc = "displayName_ASC",
  DisplayNameDesc = "displayName_DESC",
  IsRootCategoryAsc = "isRootCategory_ASC",
  IsRootCategoryDesc = "isRootCategory_DESC",
  NameAsc = "name_ASC",
  NameDesc = "name_DESC",
  SlugAsc = "slug_ASC",
  SlugDesc = "slug_DESC",
  SysFirstPublishedAtAsc = "sys_firstPublishedAt_ASC",
  SysFirstPublishedAtDesc = "sys_firstPublishedAt_DESC",
  SysIdAsc = "sys_id_ASC",
  SysIdDesc = "sys_id_DESC",
  SysPublishedAtAsc = "sys_publishedAt_ASC",
  SysPublishedAtDesc = "sys_publishedAt_DESC",
  SysPublishedVersionAsc = "sys_publishedVersion_ASC",
  SysPublishedVersionDesc = "sys_publishedVersion_DESC",
}

export enum ProductGroupOrder {
  SysFirstPublishedAtAsc = "sys_firstPublishedAt_ASC",
  SysFirstPublishedAtDesc = "sys_firstPublishedAt_DESC",
  SysIdAsc = "sys_id_ASC",
  SysIdDesc = "sys_id_DESC",
  SysPublishedAtAsc = "sys_publishedAt_ASC",
  SysPublishedAtDesc = "sys_publishedAt_DESC",
  SysPublishedVersionAsc = "sys_publishedVersion_ASC",
  SysPublishedVersionDesc = "sys_publishedVersion_DESC",
  TypeAsc = "type_ASC",
  TypeDesc = "type_DESC",
}

export type ProductGroupProductVariantsCollection = {
  __typename?: "ProductGroupProductVariantsCollection";
  items: Array<Maybe<ProductVariant>>;
  limit: Scalars["Int"]["output"];
  skip: Scalars["Int"]["output"];
  total: Scalars["Int"]["output"];
};

export enum ProductGroupProductVariantsCollectionOrder {
  ColorCodeAsc = "colorCode_ASC",
  ColorCodeDesc = "colorCode_DESC",
  ColorNameAsc = "colorName_ASC",
  ColorNameDesc = "colorName_DESC",
  FirstMediaInOverviewAsc = "firstMediaInOverview_ASC",
  FirstMediaInOverviewDesc = "firstMediaInOverview_DESC",
  PriceAsc = "price_ASC",
  PriceDesc = "price_DESC",
  RefAsc = "ref_ASC",
  RefDesc = "ref_DESC",
  SysFirstPublishedAtAsc = "sys_firstPublishedAt_ASC",
  SysFirstPublishedAtDesc = "sys_firstPublishedAt_DESC",
  SysIdAsc = "sys_id_ASC",
  SysIdDesc = "sys_id_DESC",
  SysPublishedAtAsc = "sys_publishedAt_ASC",
  SysPublishedAtDesc = "sys_publishedAt_DESC",
  SysPublishedVersionAsc = "sys_publishedVersion_ASC",
  SysPublishedVersionDesc = "sys_publishedVersion_DESC",
}

export type ProductLinkingCollections = {
  __typename?: "ProductLinkingCollections";
  entryCollection: Maybe<EntryCollection>;
};

export type ProductLinkingCollectionsEntryCollectionArgs = {
  limit?: InputMaybe<Scalars["Int"]["input"]>;
  locale: InputMaybe<Scalars["String"]["input"]>;
  preview: InputMaybe<Scalars["Boolean"]["input"]>;
  skip?: InputMaybe<Scalars["Int"]["input"]>;
};

export enum ProductOrder {
  NameAsc = "name_ASC",
  NameDesc = "name_DESC",
  SlugAsc = "slug_ASC",
  SlugDesc = "slug_DESC",
  SysFirstPublishedAtAsc = "sys_firstPublishedAt_ASC",
  SysFirstPublishedAtDesc = "sys_firstPublishedAt_DESC",
  SysIdAsc = "sys_id_ASC",
  SysIdDesc = "sys_id_DESC",
  SysPublishedAtAsc = "sys_publishedAt_ASC",
  SysPublishedAtDesc = "sys_publishedAt_DESC",
  SysPublishedVersionAsc = "sys_publishedVersion_ASC",
  SysPublishedVersionDesc = "sys_publishedVersion_DESC",
}

/** [See type definition](https://app.contentful.com/spaces/nh559twm3d3o/content_types/productVariant) */
export type ProductVariant = Entry & {
  __typename?: "ProductVariant";
  attributesCollection: Maybe<ProductVariantAttributesCollection>;
  colorCode: Maybe<Scalars["String"]["output"]>;
  colorName: Maybe<Scalars["String"]["output"]>;
  contentfulMetadata: ContentfulMetadata;
  firstMediaInOverview: Maybe<Scalars["Int"]["output"]>;
  linkedFrom: Maybe<ProductVariantLinkingCollections>;
  mediaCollection: Maybe<AssetCollection>;
  price: Maybe<Scalars["Int"]["output"]>;
  ref: Maybe<Scalars["String"]["output"]>;
  skuList: Maybe<Array<Maybe<Scalars["String"]["output"]>>>;
  sys: Sys;
};

/** [See type definition](https://app.contentful.com/spaces/nh559twm3d3o/content_types/productVariant) */
export type ProductVariantAttributesCollectionArgs = {
  limit?: InputMaybe<Scalars["Int"]["input"]>;
  locale: InputMaybe<Scalars["String"]["input"]>;
  order: InputMaybe<Array<InputMaybe<ProductVariantAttributesCollectionOrder>>>;
  preview: InputMaybe<Scalars["Boolean"]["input"]>;
  skip?: InputMaybe<Scalars["Int"]["input"]>;
  where: InputMaybe<ProductAttributeFilter>;
};

/** [See type definition](https://app.contentful.com/spaces/nh559twm3d3o/content_types/productVariant) */
export type ProductVariantColorCodeArgs = {
  locale: InputMaybe<Scalars["String"]["input"]>;
};

/** [See type definition](https://app.contentful.com/spaces/nh559twm3d3o/content_types/productVariant) */
export type ProductVariantColorNameArgs = {
  locale: InputMaybe<Scalars["String"]["input"]>;
};

/** [See type definition](https://app.contentful.com/spaces/nh559twm3d3o/content_types/productVariant) */
export type ProductVariantFirstMediaInOverviewArgs = {
  locale: InputMaybe<Scalars["String"]["input"]>;
};

/** [See type definition](https://app.contentful.com/spaces/nh559twm3d3o/content_types/productVariant) */
export type ProductVariantLinkedFromArgs = {
  allowedLocales: InputMaybe<Array<InputMaybe<Scalars["String"]["input"]>>>;
};

/** [See type definition](https://app.contentful.com/spaces/nh559twm3d3o/content_types/productVariant) */
export type ProductVariantMediaCollectionArgs = {
  limit?: InputMaybe<Scalars["Int"]["input"]>;
  locale: InputMaybe<Scalars["String"]["input"]>;
  preview: InputMaybe<Scalars["Boolean"]["input"]>;
  skip?: InputMaybe<Scalars["Int"]["input"]>;
};

/** [See type definition](https://app.contentful.com/spaces/nh559twm3d3o/content_types/productVariant) */
export type ProductVariantPriceArgs = {
  locale: InputMaybe<Scalars["String"]["input"]>;
};

/** [See type definition](https://app.contentful.com/spaces/nh559twm3d3o/content_types/productVariant) */
export type ProductVariantRefArgs = {
  locale: InputMaybe<Scalars["String"]["input"]>;
};

/** [See type definition](https://app.contentful.com/spaces/nh559twm3d3o/content_types/productVariant) */
export type ProductVariantSkuListArgs = {
  locale: InputMaybe<Scalars["String"]["input"]>;
};

export type ProductVariantAttributesCollection = {
  __typename?: "ProductVariantAttributesCollection";
  items: Array<Maybe<ProductAttribute>>;
  limit: Scalars["Int"]["output"];
  skip: Scalars["Int"]["output"];
  total: Scalars["Int"]["output"];
};

export enum ProductVariantAttributesCollectionOrder {
  NameAsc = "name_ASC",
  NameDesc = "name_DESC",
  SlugAsc = "slug_ASC",
  SlugDesc = "slug_DESC",
  SysFirstPublishedAtAsc = "sys_firstPublishedAt_ASC",
  SysFirstPublishedAtDesc = "sys_firstPublishedAt_DESC",
  SysIdAsc = "sys_id_ASC",
  SysIdDesc = "sys_id_DESC",
  SysPublishedAtAsc = "sys_publishedAt_ASC",
  SysPublishedAtDesc = "sys_publishedAt_DESC",
  SysPublishedVersionAsc = "sys_publishedVersion_ASC",
  SysPublishedVersionDesc = "sys_publishedVersion_DESC",
  TypeAsc = "type_ASC",
  TypeDesc = "type_DESC",
}

export type ProductVariantCollection = {
  __typename?: "ProductVariantCollection";
  items: Array<Maybe<ProductVariant>>;
  limit: Scalars["Int"]["output"];
  skip: Scalars["Int"]["output"];
  total: Scalars["Int"]["output"];
};

export type ProductVariantFilter = {
  AND: InputMaybe<Array<InputMaybe<ProductVariantFilter>>>;
  OR: InputMaybe<Array<InputMaybe<ProductVariantFilter>>>;
  attributes: InputMaybe<CfProductAttributeNestedFilter>;
  attributesCollection_exists: InputMaybe<Scalars["Boolean"]["input"]>;
  colorCode: InputMaybe<Scalars["String"]["input"]>;
  colorCode_contains: InputMaybe<Scalars["String"]["input"]>;
  colorCode_exists: InputMaybe<Scalars["Boolean"]["input"]>;
  colorCode_in: InputMaybe<Array<InputMaybe<Scalars["String"]["input"]>>>;
  colorCode_not: InputMaybe<Scalars["String"]["input"]>;
  colorCode_not_contains: InputMaybe<Scalars["String"]["input"]>;
  colorCode_not_in: InputMaybe<Array<InputMaybe<Scalars["String"]["input"]>>>;
  colorName: InputMaybe<Scalars["String"]["input"]>;
  colorName_contains: InputMaybe<Scalars["String"]["input"]>;
  colorName_exists: InputMaybe<Scalars["Boolean"]["input"]>;
  colorName_in: InputMaybe<Array<InputMaybe<Scalars["String"]["input"]>>>;
  colorName_not: InputMaybe<Scalars["String"]["input"]>;
  colorName_not_contains: InputMaybe<Scalars["String"]["input"]>;
  colorName_not_in: InputMaybe<Array<InputMaybe<Scalars["String"]["input"]>>>;
  contentfulMetadata: InputMaybe<ContentfulMetadataFilter>;
  firstMediaInOverview: InputMaybe<Scalars["Int"]["input"]>;
  firstMediaInOverview_exists: InputMaybe<Scalars["Boolean"]["input"]>;
  firstMediaInOverview_gt: InputMaybe<Scalars["Int"]["input"]>;
  firstMediaInOverview_gte: InputMaybe<Scalars["Int"]["input"]>;
  firstMediaInOverview_in: InputMaybe<
    Array<InputMaybe<Scalars["Int"]["input"]>>
  >;
  firstMediaInOverview_lt: InputMaybe<Scalars["Int"]["input"]>;
  firstMediaInOverview_lte: InputMaybe<Scalars["Int"]["input"]>;
  firstMediaInOverview_not: InputMaybe<Scalars["Int"]["input"]>;
  firstMediaInOverview_not_in: InputMaybe<
    Array<InputMaybe<Scalars["Int"]["input"]>>
  >;
  mediaCollection_exists: InputMaybe<Scalars["Boolean"]["input"]>;
  price: InputMaybe<Scalars["Int"]["input"]>;
  price_exists: InputMaybe<Scalars["Boolean"]["input"]>;
  price_gt: InputMaybe<Scalars["Int"]["input"]>;
  price_gte: InputMaybe<Scalars["Int"]["input"]>;
  price_in: InputMaybe<Array<InputMaybe<Scalars["Int"]["input"]>>>;
  price_lt: InputMaybe<Scalars["Int"]["input"]>;
  price_lte: InputMaybe<Scalars["Int"]["input"]>;
  price_not: InputMaybe<Scalars["Int"]["input"]>;
  price_not_in: InputMaybe<Array<InputMaybe<Scalars["Int"]["input"]>>>;
  ref: InputMaybe<Scalars["String"]["input"]>;
  ref_contains: InputMaybe<Scalars["String"]["input"]>;
  ref_exists: InputMaybe<Scalars["Boolean"]["input"]>;
  ref_in: InputMaybe<Array<InputMaybe<Scalars["String"]["input"]>>>;
  ref_not: InputMaybe<Scalars["String"]["input"]>;
  ref_not_contains: InputMaybe<Scalars["String"]["input"]>;
  ref_not_in: InputMaybe<Array<InputMaybe<Scalars["String"]["input"]>>>;
  skuList_contains_all: InputMaybe<
    Array<InputMaybe<Scalars["String"]["input"]>>
  >;
  skuList_contains_none: InputMaybe<
    Array<InputMaybe<Scalars["String"]["input"]>>
  >;
  skuList_contains_some: InputMaybe<
    Array<InputMaybe<Scalars["String"]["input"]>>
  >;
  skuList_exists: InputMaybe<Scalars["Boolean"]["input"]>;
  sys: InputMaybe<SysFilter>;
};

export type ProductVariantLinkingCollections = {
  __typename?: "ProductVariantLinkingCollections";
  entryCollection: Maybe<EntryCollection>;
  productCollection: Maybe<ProductCollection>;
  productGroupCollection: Maybe<ProductGroupCollection>;
};

export type ProductVariantLinkingCollectionsEntryCollectionArgs = {
  limit?: InputMaybe<Scalars["Int"]["input"]>;
  locale: InputMaybe<Scalars["String"]["input"]>;
  preview: InputMaybe<Scalars["Boolean"]["input"]>;
  skip?: InputMaybe<Scalars["Int"]["input"]>;
};

export type ProductVariantLinkingCollectionsProductCollectionArgs = {
  limit?: InputMaybe<Scalars["Int"]["input"]>;
  locale: InputMaybe<Scalars["String"]["input"]>;
  order: InputMaybe<
    Array<InputMaybe<ProductVariantLinkingCollectionsProductCollectionOrder>>
  >;
  preview: InputMaybe<Scalars["Boolean"]["input"]>;
  skip?: InputMaybe<Scalars["Int"]["input"]>;
};

export type ProductVariantLinkingCollectionsProductGroupCollectionArgs = {
  limit?: InputMaybe<Scalars["Int"]["input"]>;
  locale: InputMaybe<Scalars["String"]["input"]>;
  order: InputMaybe<
    Array<
      InputMaybe<ProductVariantLinkingCollectionsProductGroupCollectionOrder>
    >
  >;
  preview: InputMaybe<Scalars["Boolean"]["input"]>;
  skip?: InputMaybe<Scalars["Int"]["input"]>;
};

export enum ProductVariantLinkingCollectionsProductCollectionOrder {
  NameAsc = "name_ASC",
  NameDesc = "name_DESC",
  SlugAsc = "slug_ASC",
  SlugDesc = "slug_DESC",
  SysFirstPublishedAtAsc = "sys_firstPublishedAt_ASC",
  SysFirstPublishedAtDesc = "sys_firstPublishedAt_DESC",
  SysIdAsc = "sys_id_ASC",
  SysIdDesc = "sys_id_DESC",
  SysPublishedAtAsc = "sys_publishedAt_ASC",
  SysPublishedAtDesc = "sys_publishedAt_DESC",
  SysPublishedVersionAsc = "sys_publishedVersion_ASC",
  SysPublishedVersionDesc = "sys_publishedVersion_DESC",
}

export enum ProductVariantLinkingCollectionsProductGroupCollectionOrder {
  SysFirstPublishedAtAsc = "sys_firstPublishedAt_ASC",
  SysFirstPublishedAtDesc = "sys_firstPublishedAt_DESC",
  SysIdAsc = "sys_id_ASC",
  SysIdDesc = "sys_id_DESC",
  SysPublishedAtAsc = "sys_publishedAt_ASC",
  SysPublishedAtDesc = "sys_publishedAt_DESC",
  SysPublishedVersionAsc = "sys_publishedVersion_ASC",
  SysPublishedVersionDesc = "sys_publishedVersion_DESC",
  TypeAsc = "type_ASC",
  TypeDesc = "type_DESC",
}

export enum ProductVariantOrder {
  ColorCodeAsc = "colorCode_ASC",
  ColorCodeDesc = "colorCode_DESC",
  ColorNameAsc = "colorName_ASC",
  ColorNameDesc = "colorName_DESC",
  FirstMediaInOverviewAsc = "firstMediaInOverview_ASC",
  FirstMediaInOverviewDesc = "firstMediaInOverview_DESC",
  PriceAsc = "price_ASC",
  PriceDesc = "price_DESC",
  RefAsc = "ref_ASC",
  RefDesc = "ref_DESC",
  SysFirstPublishedAtAsc = "sys_firstPublishedAt_ASC",
  SysFirstPublishedAtDesc = "sys_firstPublishedAt_DESC",
  SysIdAsc = "sys_id_ASC",
  SysIdDesc = "sys_id_DESC",
  SysPublishedAtAsc = "sys_publishedAt_ASC",
  SysPublishedAtDesc = "sys_publishedAt_DESC",
  SysPublishedVersionAsc = "sys_publishedVersion_ASC",
  SysPublishedVersionDesc = "sys_publishedVersion_DESC",
}

export type ProductVariantsCollection = {
  __typename?: "ProductVariantsCollection";
  items: Array<Maybe<ProductVariant>>;
  limit: Scalars["Int"]["output"];
  skip: Scalars["Int"]["output"];
  total: Scalars["Int"]["output"];
};

export enum ProductVariantsCollectionOrder {
  ColorCodeAsc = "colorCode_ASC",
  ColorCodeDesc = "colorCode_DESC",
  ColorNameAsc = "colorName_ASC",
  ColorNameDesc = "colorName_DESC",
  FirstMediaInOverviewAsc = "firstMediaInOverview_ASC",
  FirstMediaInOverviewDesc = "firstMediaInOverview_DESC",
  PriceAsc = "price_ASC",
  PriceDesc = "price_DESC",
  RefAsc = "ref_ASC",
  RefDesc = "ref_DESC",
  SysFirstPublishedAtAsc = "sys_firstPublishedAt_ASC",
  SysFirstPublishedAtDesc = "sys_firstPublishedAt_DESC",
  SysIdAsc = "sys_id_ASC",
  SysIdDesc = "sys_id_DESC",
  SysPublishedAtAsc = "sys_publishedAt_ASC",
  SysPublishedAtDesc = "sys_publishedAt_DESC",
  SysPublishedVersionAsc = "sys_publishedVersion_ASC",
  SysPublishedVersionDesc = "sys_publishedVersion_DESC",
}

export type Query = {
  __typename?: "Query";
  asset: Maybe<Asset>;
  assetCollection: Maybe<AssetCollection>;
  categories: Maybe<Categories>;
  categoriesCollection: Maybe<CategoriesCollection>;
  category: Maybe<Category>;
  categoryCollection: Maybe<CategoryCollection>;
  categoryHighlight: Maybe<CategoryHighlight>;
  categoryHighlightCollection: Maybe<CategoryHighlightCollection>;
  entryCollection: Maybe<EntryCollection>;
  highlightSlide: Maybe<HighlightSlide>;
  highlightSlideCollection: Maybe<HighlightSlideCollection>;
  product: Maybe<Product>;
  productAttribute: Maybe<ProductAttribute>;
  productAttributeCollection: Maybe<ProductAttributeCollection>;
  productCollection: Maybe<ProductCollection>;
  productGroup: Maybe<ProductGroup>;
  productGroupCollection: Maybe<ProductGroupCollection>;
  productVariant: Maybe<ProductVariant>;
  productVariantCollection: Maybe<ProductVariantCollection>;
};

export type QueryAssetArgs = {
  id: Scalars["String"]["input"];
  locale: InputMaybe<Scalars["String"]["input"]>;
  preview: InputMaybe<Scalars["Boolean"]["input"]>;
};

export type QueryAssetCollectionArgs = {
  limit?: InputMaybe<Scalars["Int"]["input"]>;
  locale: InputMaybe<Scalars["String"]["input"]>;
  order: InputMaybe<Array<InputMaybe<AssetOrder>>>;
  preview: InputMaybe<Scalars["Boolean"]["input"]>;
  skip?: InputMaybe<Scalars["Int"]["input"]>;
  where: InputMaybe<AssetFilter>;
};

export type QueryCategoriesArgs = {
  id: Scalars["String"]["input"];
  locale: InputMaybe<Scalars["String"]["input"]>;
  preview: InputMaybe<Scalars["Boolean"]["input"]>;
};

export type QueryCategoriesCollectionArgs = {
  limit?: InputMaybe<Scalars["Int"]["input"]>;
  locale: InputMaybe<Scalars["String"]["input"]>;
  order: InputMaybe<Array<InputMaybe<CategoriesOrder>>>;
  preview: InputMaybe<Scalars["Boolean"]["input"]>;
  skip?: InputMaybe<Scalars["Int"]["input"]>;
  where: InputMaybe<CategoriesFilter>;
};

export type QueryCategoryArgs = {
  id: Scalars["String"]["input"];
  locale: InputMaybe<Scalars["String"]["input"]>;
  preview: InputMaybe<Scalars["Boolean"]["input"]>;
};

export type QueryCategoryCollectionArgs = {
  limit?: InputMaybe<Scalars["Int"]["input"]>;
  locale: InputMaybe<Scalars["String"]["input"]>;
  order: InputMaybe<Array<InputMaybe<CategoryOrder>>>;
  preview: InputMaybe<Scalars["Boolean"]["input"]>;
  skip?: InputMaybe<Scalars["Int"]["input"]>;
  where: InputMaybe<CategoryFilter>;
};

export type QueryCategoryHighlightArgs = {
  id: Scalars["String"]["input"];
  locale: InputMaybe<Scalars["String"]["input"]>;
  preview: InputMaybe<Scalars["Boolean"]["input"]>;
};

export type QueryCategoryHighlightCollectionArgs = {
  limit?: InputMaybe<Scalars["Int"]["input"]>;
  locale: InputMaybe<Scalars["String"]["input"]>;
  order: InputMaybe<Array<InputMaybe<CategoryHighlightOrder>>>;
  preview: InputMaybe<Scalars["Boolean"]["input"]>;
  skip?: InputMaybe<Scalars["Int"]["input"]>;
  where: InputMaybe<CategoryHighlightFilter>;
};

export type QueryEntryCollectionArgs = {
  limit?: InputMaybe<Scalars["Int"]["input"]>;
  locale: InputMaybe<Scalars["String"]["input"]>;
  order: InputMaybe<Array<InputMaybe<EntryOrder>>>;
  preview: InputMaybe<Scalars["Boolean"]["input"]>;
  skip?: InputMaybe<Scalars["Int"]["input"]>;
  where: InputMaybe<EntryFilter>;
};

export type QueryHighlightSlideArgs = {
  id: Scalars["String"]["input"];
  locale: InputMaybe<Scalars["String"]["input"]>;
  preview: InputMaybe<Scalars["Boolean"]["input"]>;
};

export type QueryHighlightSlideCollectionArgs = {
  limit?: InputMaybe<Scalars["Int"]["input"]>;
  locale: InputMaybe<Scalars["String"]["input"]>;
  order: InputMaybe<Array<InputMaybe<HighlightSlideOrder>>>;
  preview: InputMaybe<Scalars["Boolean"]["input"]>;
  skip?: InputMaybe<Scalars["Int"]["input"]>;
  where: InputMaybe<HighlightSlideFilter>;
};

export type QueryProductArgs = {
  id: Scalars["String"]["input"];
  locale: InputMaybe<Scalars["String"]["input"]>;
  preview: InputMaybe<Scalars["Boolean"]["input"]>;
};

export type QueryProductAttributeArgs = {
  id: Scalars["String"]["input"];
  locale: InputMaybe<Scalars["String"]["input"]>;
  preview: InputMaybe<Scalars["Boolean"]["input"]>;
};

export type QueryProductAttributeCollectionArgs = {
  limit?: InputMaybe<Scalars["Int"]["input"]>;
  locale: InputMaybe<Scalars["String"]["input"]>;
  order: InputMaybe<Array<InputMaybe<ProductAttributeOrder>>>;
  preview: InputMaybe<Scalars["Boolean"]["input"]>;
  skip?: InputMaybe<Scalars["Int"]["input"]>;
  where: InputMaybe<ProductAttributeFilter>;
};

export type QueryProductCollectionArgs = {
  limit?: InputMaybe<Scalars["Int"]["input"]>;
  locale: InputMaybe<Scalars["String"]["input"]>;
  order: InputMaybe<Array<InputMaybe<ProductOrder>>>;
  preview: InputMaybe<Scalars["Boolean"]["input"]>;
  skip?: InputMaybe<Scalars["Int"]["input"]>;
  where: InputMaybe<ProductFilter>;
};

export type QueryProductGroupArgs = {
  id: Scalars["String"]["input"];
  locale: InputMaybe<Scalars["String"]["input"]>;
  preview: InputMaybe<Scalars["Boolean"]["input"]>;
};

export type QueryProductGroupCollectionArgs = {
  limit?: InputMaybe<Scalars["Int"]["input"]>;
  locale: InputMaybe<Scalars["String"]["input"]>;
  order: InputMaybe<Array<InputMaybe<ProductGroupOrder>>>;
  preview: InputMaybe<Scalars["Boolean"]["input"]>;
  skip?: InputMaybe<Scalars["Int"]["input"]>;
  where: InputMaybe<ProductGroupFilter>;
};

export type QueryProductVariantArgs = {
  id: Scalars["String"]["input"];
  locale: InputMaybe<Scalars["String"]["input"]>;
  preview: InputMaybe<Scalars["Boolean"]["input"]>;
};

export type QueryProductVariantCollectionArgs = {
  limit?: InputMaybe<Scalars["Int"]["input"]>;
  locale: InputMaybe<Scalars["String"]["input"]>;
  order: InputMaybe<Array<InputMaybe<ProductVariantOrder>>>;
  preview: InputMaybe<Scalars["Boolean"]["input"]>;
  skip?: InputMaybe<Scalars["Int"]["input"]>;
  where: InputMaybe<ProductVariantFilter>;
};

export type Sys = {
  __typename?: "Sys";
  environmentId: Scalars["String"]["output"];
  firstPublishedAt: Maybe<Scalars["DateTime"]["output"]>;
  id: Scalars["String"]["output"];
  publishedAt: Maybe<Scalars["DateTime"]["output"]>;
  publishedVersion: Maybe<Scalars["Int"]["output"]>;
  spaceId: Scalars["String"]["output"];
};

export type SysFilter = {
  firstPublishedAt: InputMaybe<Scalars["DateTime"]["input"]>;
  firstPublishedAt_exists: InputMaybe<Scalars["Boolean"]["input"]>;
  firstPublishedAt_gt: InputMaybe<Scalars["DateTime"]["input"]>;
  firstPublishedAt_gte: InputMaybe<Scalars["DateTime"]["input"]>;
  firstPublishedAt_in: InputMaybe<
    Array<InputMaybe<Scalars["DateTime"]["input"]>>
  >;
  firstPublishedAt_lt: InputMaybe<Scalars["DateTime"]["input"]>;
  firstPublishedAt_lte: InputMaybe<Scalars["DateTime"]["input"]>;
  firstPublishedAt_not: InputMaybe<Scalars["DateTime"]["input"]>;
  firstPublishedAt_not_in: InputMaybe<
    Array<InputMaybe<Scalars["DateTime"]["input"]>>
  >;
  id: InputMaybe<Scalars["String"]["input"]>;
  id_contains: InputMaybe<Scalars["String"]["input"]>;
  id_exists: InputMaybe<Scalars["Boolean"]["input"]>;
  id_in: InputMaybe<Array<InputMaybe<Scalars["String"]["input"]>>>;
  id_not: InputMaybe<Scalars["String"]["input"]>;
  id_not_contains: InputMaybe<Scalars["String"]["input"]>;
  id_not_in: InputMaybe<Array<InputMaybe<Scalars["String"]["input"]>>>;
  publishedAt: InputMaybe<Scalars["DateTime"]["input"]>;
  publishedAt_exists: InputMaybe<Scalars["Boolean"]["input"]>;
  publishedAt_gt: InputMaybe<Scalars["DateTime"]["input"]>;
  publishedAt_gte: InputMaybe<Scalars["DateTime"]["input"]>;
  publishedAt_in: InputMaybe<Array<InputMaybe<Scalars["DateTime"]["input"]>>>;
  publishedAt_lt: InputMaybe<Scalars["DateTime"]["input"]>;
  publishedAt_lte: InputMaybe<Scalars["DateTime"]["input"]>;
  publishedAt_not: InputMaybe<Scalars["DateTime"]["input"]>;
  publishedAt_not_in: InputMaybe<
    Array<InputMaybe<Scalars["DateTime"]["input"]>>
  >;
  publishedVersion: InputMaybe<Scalars["Float"]["input"]>;
  publishedVersion_exists: InputMaybe<Scalars["Boolean"]["input"]>;
  publishedVersion_gt: InputMaybe<Scalars["Float"]["input"]>;
  publishedVersion_gte: InputMaybe<Scalars["Float"]["input"]>;
  publishedVersion_in: InputMaybe<Array<InputMaybe<Scalars["Float"]["input"]>>>;
  publishedVersion_lt: InputMaybe<Scalars["Float"]["input"]>;
  publishedVersion_lte: InputMaybe<Scalars["Float"]["input"]>;
  publishedVersion_not: InputMaybe<Scalars["Float"]["input"]>;
  publishedVersion_not_in: InputMaybe<
    Array<InputMaybe<Scalars["Float"]["input"]>>
  >;
};

export type CfCategoryNestedFilter = {
  AND: InputMaybe<Array<InputMaybe<CfCategoryNestedFilter>>>;
  OR: InputMaybe<Array<InputMaybe<CfCategoryNestedFilter>>>;
  autoFillSchema: InputMaybe<Scalars["String"]["input"]>;
  autoFillSchema_contains: InputMaybe<Scalars["String"]["input"]>;
  autoFillSchema_exists: InputMaybe<Scalars["Boolean"]["input"]>;
  autoFillSchema_in: InputMaybe<Array<InputMaybe<Scalars["String"]["input"]>>>;
  autoFillSchema_not: InputMaybe<Scalars["String"]["input"]>;
  autoFillSchema_not_contains: InputMaybe<Scalars["String"]["input"]>;
  autoFillSchema_not_in: InputMaybe<
    Array<InputMaybe<Scalars["String"]["input"]>>
  >;
  contentfulMetadata: InputMaybe<ContentfulMetadataFilter>;
  customProductGroupCollection_exists: InputMaybe<Scalars["Boolean"]["input"]>;
  displayName: InputMaybe<Scalars["String"]["input"]>;
  displayName_contains: InputMaybe<Scalars["String"]["input"]>;
  displayName_exists: InputMaybe<Scalars["Boolean"]["input"]>;
  displayName_in: InputMaybe<Array<InputMaybe<Scalars["String"]["input"]>>>;
  displayName_not: InputMaybe<Scalars["String"]["input"]>;
  displayName_not_contains: InputMaybe<Scalars["String"]["input"]>;
  displayName_not_in: InputMaybe<Array<InputMaybe<Scalars["String"]["input"]>>>;
  intersectAttributesCollection_exists: InputMaybe<Scalars["Boolean"]["input"]>;
  isRootCategory: InputMaybe<Scalars["Boolean"]["input"]>;
  isRootCategory_exists: InputMaybe<Scalars["Boolean"]["input"]>;
  isRootCategory_not: InputMaybe<Scalars["Boolean"]["input"]>;
  name: InputMaybe<Scalars["String"]["input"]>;
  name_contains: InputMaybe<Scalars["String"]["input"]>;
  name_exists: InputMaybe<Scalars["Boolean"]["input"]>;
  name_in: InputMaybe<Array<InputMaybe<Scalars["String"]["input"]>>>;
  name_not: InputMaybe<Scalars["String"]["input"]>;
  name_not_contains: InputMaybe<Scalars["String"]["input"]>;
  name_not_in: InputMaybe<Array<InputMaybe<Scalars["String"]["input"]>>>;
  slug: InputMaybe<Scalars["String"]["input"]>;
  slug_contains: InputMaybe<Scalars["String"]["input"]>;
  slug_exists: InputMaybe<Scalars["Boolean"]["input"]>;
  slug_in: InputMaybe<Array<InputMaybe<Scalars["String"]["input"]>>>;
  slug_not: InputMaybe<Scalars["String"]["input"]>;
  slug_not_contains: InputMaybe<Scalars["String"]["input"]>;
  slug_not_in: InputMaybe<Array<InputMaybe<Scalars["String"]["input"]>>>;
  subCategoriesCollection_exists: InputMaybe<Scalars["Boolean"]["input"]>;
  sys: InputMaybe<SysFilter>;
  unionAttributesCollection_exists: InputMaybe<Scalars["Boolean"]["input"]>;
};

export type CfHighlightSlideNestedFilter = {
  AND: InputMaybe<Array<InputMaybe<CfHighlightSlideNestedFilter>>>;
  OR: InputMaybe<Array<InputMaybe<CfHighlightSlideNestedFilter>>>;
  category_exists: InputMaybe<Scalars["Boolean"]["input"]>;
  contentfulMetadata: InputMaybe<ContentfulMetadataFilter>;
  href: InputMaybe<Scalars["String"]["input"]>;
  href_contains: InputMaybe<Scalars["String"]["input"]>;
  href_exists: InputMaybe<Scalars["Boolean"]["input"]>;
  href_in: InputMaybe<Array<InputMaybe<Scalars["String"]["input"]>>>;
  href_not: InputMaybe<Scalars["String"]["input"]>;
  href_not_contains: InputMaybe<Scalars["String"]["input"]>;
  href_not_in: InputMaybe<Array<InputMaybe<Scalars["String"]["input"]>>>;
  media_exists: InputMaybe<Scalars["Boolean"]["input"]>;
  name: InputMaybe<Scalars["String"]["input"]>;
  name_contains: InputMaybe<Scalars["String"]["input"]>;
  name_exists: InputMaybe<Scalars["Boolean"]["input"]>;
  name_in: InputMaybe<Array<InputMaybe<Scalars["String"]["input"]>>>;
  name_not: InputMaybe<Scalars["String"]["input"]>;
  name_not_contains: InputMaybe<Scalars["String"]["input"]>;
  name_not_in: InputMaybe<Array<InputMaybe<Scalars["String"]["input"]>>>;
  rootCategorySlug: InputMaybe<Scalars["String"]["input"]>;
  rootCategorySlug_contains: InputMaybe<Scalars["String"]["input"]>;
  rootCategorySlug_exists: InputMaybe<Scalars["Boolean"]["input"]>;
  rootCategorySlug_in: InputMaybe<
    Array<InputMaybe<Scalars["String"]["input"]>>
  >;
  rootCategorySlug_not: InputMaybe<Scalars["String"]["input"]>;
  rootCategorySlug_not_contains: InputMaybe<Scalars["String"]["input"]>;
  rootCategorySlug_not_in: InputMaybe<
    Array<InputMaybe<Scalars["String"]["input"]>>
  >;
  shouldRedirect: InputMaybe<Scalars["Boolean"]["input"]>;
  shouldRedirect_exists: InputMaybe<Scalars["Boolean"]["input"]>;
  shouldRedirect_not: InputMaybe<Scalars["Boolean"]["input"]>;
  sys: InputMaybe<SysFilter>;
  theme: InputMaybe<Scalars["String"]["input"]>;
  theme_contains: InputMaybe<Scalars["String"]["input"]>;
  theme_exists: InputMaybe<Scalars["Boolean"]["input"]>;
  theme_in: InputMaybe<Array<InputMaybe<Scalars["String"]["input"]>>>;
  theme_not: InputMaybe<Scalars["String"]["input"]>;
  theme_not_contains: InputMaybe<Scalars["String"]["input"]>;
  theme_not_in: InputMaybe<Array<InputMaybe<Scalars["String"]["input"]>>>;
};

export type CfProductAttributeNestedFilter = {
  AND: InputMaybe<Array<InputMaybe<CfProductAttributeNestedFilter>>>;
  OR: InputMaybe<Array<InputMaybe<CfProductAttributeNestedFilter>>>;
  contentfulMetadata: InputMaybe<ContentfulMetadataFilter>;
  name: InputMaybe<Scalars["String"]["input"]>;
  name_contains: InputMaybe<Scalars["String"]["input"]>;
  name_exists: InputMaybe<Scalars["Boolean"]["input"]>;
  name_in: InputMaybe<Array<InputMaybe<Scalars["String"]["input"]>>>;
  name_not: InputMaybe<Scalars["String"]["input"]>;
  name_not_contains: InputMaybe<Scalars["String"]["input"]>;
  name_not_in: InputMaybe<Array<InputMaybe<Scalars["String"]["input"]>>>;
  slug: InputMaybe<Scalars["String"]["input"]>;
  slug_contains: InputMaybe<Scalars["String"]["input"]>;
  slug_exists: InputMaybe<Scalars["Boolean"]["input"]>;
  slug_in: InputMaybe<Array<InputMaybe<Scalars["String"]["input"]>>>;
  slug_not: InputMaybe<Scalars["String"]["input"]>;
  slug_not_contains: InputMaybe<Scalars["String"]["input"]>;
  slug_not_in: InputMaybe<Array<InputMaybe<Scalars["String"]["input"]>>>;
  sys: InputMaybe<SysFilter>;
  type: InputMaybe<Scalars["String"]["input"]>;
  type_contains: InputMaybe<Scalars["String"]["input"]>;
  type_exists: InputMaybe<Scalars["Boolean"]["input"]>;
  type_in: InputMaybe<Array<InputMaybe<Scalars["String"]["input"]>>>;
  type_not: InputMaybe<Scalars["String"]["input"]>;
  type_not_contains: InputMaybe<Scalars["String"]["input"]>;
  type_not_in: InputMaybe<Array<InputMaybe<Scalars["String"]["input"]>>>;
  valuesCollection_exists: InputMaybe<Scalars["Boolean"]["input"]>;
};

export type CfProductGroupNestedFilter = {
  AND: InputMaybe<Array<InputMaybe<CfProductGroupNestedFilter>>>;
  OR: InputMaybe<Array<InputMaybe<CfProductGroupNestedFilter>>>;
  contentfulMetadata: InputMaybe<ContentfulMetadataFilter>;
  firstMediaOfEachVariant_contains_all: InputMaybe<
    Array<InputMaybe<Scalars["String"]["input"]>>
  >;
  firstMediaOfEachVariant_contains_none: InputMaybe<
    Array<InputMaybe<Scalars["String"]["input"]>>
  >;
  firstMediaOfEachVariant_contains_some: InputMaybe<
    Array<InputMaybe<Scalars["String"]["input"]>>
  >;
  firstMediaOfEachVariant_exists: InputMaybe<Scalars["Boolean"]["input"]>;
  highlightMedia_exists: InputMaybe<Scalars["Boolean"]["input"]>;
  productVariantsCollection_exists: InputMaybe<Scalars["Boolean"]["input"]>;
  sys: InputMaybe<SysFilter>;
  type: InputMaybe<Scalars["String"]["input"]>;
  type_contains: InputMaybe<Scalars["String"]["input"]>;
  type_exists: InputMaybe<Scalars["Boolean"]["input"]>;
  type_in: InputMaybe<Array<InputMaybe<Scalars["String"]["input"]>>>;
  type_not: InputMaybe<Scalars["String"]["input"]>;
  type_not_contains: InputMaybe<Scalars["String"]["input"]>;
  type_not_in: InputMaybe<Array<InputMaybe<Scalars["String"]["input"]>>>;
};

export type CfProductVariantNestedFilter = {
  AND: InputMaybe<Array<InputMaybe<CfProductVariantNestedFilter>>>;
  OR: InputMaybe<Array<InputMaybe<CfProductVariantNestedFilter>>>;
  attributesCollection_exists: InputMaybe<Scalars["Boolean"]["input"]>;
  colorCode: InputMaybe<Scalars["String"]["input"]>;
  colorCode_contains: InputMaybe<Scalars["String"]["input"]>;
  colorCode_exists: InputMaybe<Scalars["Boolean"]["input"]>;
  colorCode_in: InputMaybe<Array<InputMaybe<Scalars["String"]["input"]>>>;
  colorCode_not: InputMaybe<Scalars["String"]["input"]>;
  colorCode_not_contains: InputMaybe<Scalars["String"]["input"]>;
  colorCode_not_in: InputMaybe<Array<InputMaybe<Scalars["String"]["input"]>>>;
  colorName: InputMaybe<Scalars["String"]["input"]>;
  colorName_contains: InputMaybe<Scalars["String"]["input"]>;
  colorName_exists: InputMaybe<Scalars["Boolean"]["input"]>;
  colorName_in: InputMaybe<Array<InputMaybe<Scalars["String"]["input"]>>>;
  colorName_not: InputMaybe<Scalars["String"]["input"]>;
  colorName_not_contains: InputMaybe<Scalars["String"]["input"]>;
  colorName_not_in: InputMaybe<Array<InputMaybe<Scalars["String"]["input"]>>>;
  contentfulMetadata: InputMaybe<ContentfulMetadataFilter>;
  firstMediaInOverview: InputMaybe<Scalars["Int"]["input"]>;
  firstMediaInOverview_exists: InputMaybe<Scalars["Boolean"]["input"]>;
  firstMediaInOverview_gt: InputMaybe<Scalars["Int"]["input"]>;
  firstMediaInOverview_gte: InputMaybe<Scalars["Int"]["input"]>;
  firstMediaInOverview_in: InputMaybe<
    Array<InputMaybe<Scalars["Int"]["input"]>>
  >;
  firstMediaInOverview_lt: InputMaybe<Scalars["Int"]["input"]>;
  firstMediaInOverview_lte: InputMaybe<Scalars["Int"]["input"]>;
  firstMediaInOverview_not: InputMaybe<Scalars["Int"]["input"]>;
  firstMediaInOverview_not_in: InputMaybe<
    Array<InputMaybe<Scalars["Int"]["input"]>>
  >;
  mediaCollection_exists: InputMaybe<Scalars["Boolean"]["input"]>;
  price: InputMaybe<Scalars["Int"]["input"]>;
  price_exists: InputMaybe<Scalars["Boolean"]["input"]>;
  price_gt: InputMaybe<Scalars["Int"]["input"]>;
  price_gte: InputMaybe<Scalars["Int"]["input"]>;
  price_in: InputMaybe<Array<InputMaybe<Scalars["Int"]["input"]>>>;
  price_lt: InputMaybe<Scalars["Int"]["input"]>;
  price_lte: InputMaybe<Scalars["Int"]["input"]>;
  price_not: InputMaybe<Scalars["Int"]["input"]>;
  price_not_in: InputMaybe<Array<InputMaybe<Scalars["Int"]["input"]>>>;
  ref: InputMaybe<Scalars["String"]["input"]>;
  ref_contains: InputMaybe<Scalars["String"]["input"]>;
  ref_exists: InputMaybe<Scalars["Boolean"]["input"]>;
  ref_in: InputMaybe<Array<InputMaybe<Scalars["String"]["input"]>>>;
  ref_not: InputMaybe<Scalars["String"]["input"]>;
  ref_not_contains: InputMaybe<Scalars["String"]["input"]>;
  ref_not_in: InputMaybe<Array<InputMaybe<Scalars["String"]["input"]>>>;
  skuList_contains_all: InputMaybe<
    Array<InputMaybe<Scalars["String"]["input"]>>
  >;
  skuList_contains_none: InputMaybe<
    Array<InputMaybe<Scalars["String"]["input"]>>
  >;
  skuList_contains_some: InputMaybe<
    Array<InputMaybe<Scalars["String"]["input"]>>
  >;
  skuList_exists: InputMaybe<Scalars["Boolean"]["input"]>;
  sys: InputMaybe<SysFilter>;
};

export type FetchCategoriesQueryVariables = Exact<{
  lang: Scalars["String"]["input"];
}>;

export type FetchCategoriesQuery = {
  __typename?: "Query";
  categories: {
    __typename?: "Categories";
    categoriesCollection: {
      __typename?: "CategoriesCategoriesCollection";
      items: Array<{
        __typename?: "Category";
        name: string | null;
        isRootCategory: boolean | null;
        displayName: string | null;
        slug: string | null;
        sys: { __typename?: "Sys"; id: string };
        subCategoriesCollection: {
          __typename?: "CategorySubCategoriesCollection";
          items: Array<{
            __typename?: "Category";
            name: string | null;
            isRootCategory: boolean | null;
            displayName: string | null;
            slug: string | null;
            sys: { __typename?: "Sys"; id: string };
          } | null>;
        } | null;
      } | null>;
    } | null;
  } | null;
};

export type FetchCategoryAttributesQueryVariables = Exact<{
  categorySlug: Scalars["String"]["input"];
}>;

export type FetchCategoryAttributesQuery = {
  __typename?: "Query";
  categoryCollection: {
    __typename?: "CategoryCollection";
    items: Array<{
      __typename?: "Category";
      unionAttributesCollection: {
        __typename?: "CategoryUnionAttributesCollection";
        items: Array<{
          __typename?: "ProductAttribute";
          slug: string | null;
          sys: { __typename?: "Sys"; id: string };
        } | null>;
      } | null;
      intersectAttributesCollection: {
        __typename?: "CategoryIntersectAttributesCollection";
        items: Array<{
          __typename?: "ProductAttribute";
          slug: string | null;
          sys: { __typename?: "Sys"; id: string };
        } | null>;
      } | null;
    } | null>;
  } | null;
};

export type FetchCategoryHighlightsQueryVariables = Exact<{
  [key: string]: never;
}>;

export type FetchCategoryHighlightsQuery = {
  __typename?: "Query";
  categoryHighlightCollection: {
    __typename?: "CategoryHighlightCollection";
    items: Array<{
      __typename?: "CategoryHighlight";
      category: { __typename?: "Category"; slug: string | null } | null;
      highlightSlidesCollection: {
        __typename?: "CategoryHighlightHighlightSlidesCollection";
        items: Array<{
          __typename?: "HighlightSlide";
          theme: string | null;
          media: { __typename?: "Asset"; url: string | null } | null;
          category: {
            __typename?: "Category";
            slug: string | null;
            displayName: string | null;
          } | null;
        } | null>;
      } | null;
    } | null>;
  } | null;
};

export type FetchProductQueryVariables = Exact<{
  productSlug: Scalars["String"]["input"];
}>;

export type FetchProductQuery = {
  __typename?: "Query";
  productCollection: {
    __typename?: "ProductCollection";
    items: Array<{
      __typename?: "Product";
      name: string | null;
      description: string | null;
      slug: string | null;
      variantsCollection: {
        __typename?: "ProductVariantsCollection";
        items: Array<{
          __typename?: "ProductVariant";
          ref: string | null;
          colorName: string | null;
          colorCode: string | null;
          price: number | null;
          skuList: Array<string | null> | null;
          firstMediaInOverview: number | null;
          attributesCollection: {
            __typename?: "ProductVariantAttributesCollection";
            items: Array<{
              __typename?: "ProductAttribute";
              slug: string | null;
              name: string | null;
            } | null>;
          } | null;
          mediaCollection: {
            __typename?: "AssetCollection";
            items: Array<{ __typename?: "Asset"; url: string | null } | null>;
          } | null;
        } | null>;
      } | null;
    } | null>;
  } | null;
};

export type FetchProductVariantsInCategoryQueryVariables = Exact<{
  intersectCondition: InputMaybe<
    Array<ProductVariantFilter> | ProductVariantFilter
  >;
  unionCondition: InputMaybe<
    Array<ProductVariantFilter> | ProductVariantFilter
  >;
}>;

export type FetchProductVariantsInCategoryQuery = {
  __typename?: "Query";
  productVariantCollection: {
    __typename?: "ProductVariantCollection";
    items: Array<{
      __typename?: "ProductVariant";
      ref: string | null;
      price: number | null;
      firstMediaInOverview: number | null;
      skuList: Array<string | null> | null;
      linkedFrom: {
        __typename?: "ProductVariantLinkingCollections";
        productCollection: {
          __typename?: "ProductCollection";
          items: Array<{
            __typename?: "Product";
            slug: string | null;
            name: string | null;
            variantsCollection: {
              __typename?: "ProductVariantsCollection";
              total: number;
            } | null;
          } | null>;
        } | null;
      } | null;
      attributesCollection: {
        __typename?: "ProductVariantAttributesCollection";
        items: Array<{
          __typename?: "ProductAttribute";
          slug: string | null;
          type: string | null;
          name: string | null;
        } | null>;
      } | null;
      mediaCollection: {
        __typename?: "AssetCollection";
        items: Array<{ __typename?: "Asset"; url: string | null } | null>;
      } | null;
    } | null>;
  } | null;
};

export const FetchCategoriesDocument = {
  kind: "Document",
  definitions: [
    {
      kind: "OperationDefinition",
      operation: "query",
      name: { kind: "Name", value: "FetchCategories" },
      variableDefinitions: [
        {
          kind: "VariableDefinition",
          variable: { kind: "Variable", name: { kind: "Name", value: "lang" } },
          type: {
            kind: "NonNullType",
            type: {
              kind: "NamedType",
              name: { kind: "Name", value: "String" },
            },
          },
        },
      ],
      selectionSet: {
        kind: "SelectionSet",
        selections: [
          {
            kind: "Field",
            name: { kind: "Name", value: "categories" },
            arguments: [
              {
                kind: "Argument",
                name: { kind: "Name", value: "id" },
                value: {
                  kind: "StringValue",
                  value: "1Dxj0jPKVb5TgkZ2RYRp7x",
                  block: false,
                },
              },
              {
                kind: "Argument",
                name: { kind: "Name", value: "locale" },
                value: {
                  kind: "Variable",
                  name: { kind: "Name", value: "lang" },
                },
              },
            ],
            selectionSet: {
              kind: "SelectionSet",
              selections: [
                {
                  kind: "Field",
                  name: { kind: "Name", value: "categoriesCollection" },
                  arguments: [
                    {
                      kind: "Argument",
                      name: { kind: "Name", value: "limit" },
                      value: { kind: "IntValue", value: "3" },
                    },
                  ],
                  selectionSet: {
                    kind: "SelectionSet",
                    selections: [
                      {
                        kind: "Field",
                        name: { kind: "Name", value: "items" },
                        selectionSet: {
                          kind: "SelectionSet",
                          selections: [
                            {
                              kind: "Field",
                              name: { kind: "Name", value: "sys" },
                              selectionSet: {
                                kind: "SelectionSet",
                                selections: [
                                  {
                                    kind: "Field",
                                    name: { kind: "Name", value: "id" },
                                  },
                                ],
                              },
                            },
                            {
                              kind: "Field",
                              name: { kind: "Name", value: "name" },
                            },
                            {
                              kind: "Field",
                              name: { kind: "Name", value: "isRootCategory" },
                            },
                            {
                              kind: "Field",
                              name: { kind: "Name", value: "displayName" },
                            },
                            {
                              kind: "Field",
                              name: { kind: "Name", value: "slug" },
                            },
                            {
                              kind: "Field",
                              name: {
                                kind: "Name",
                                value: "subCategoriesCollection",
                              },
                              selectionSet: {
                                kind: "SelectionSet",
                                selections: [
                                  {
                                    kind: "Field",
                                    name: { kind: "Name", value: "items" },
                                    selectionSet: {
                                      kind: "SelectionSet",
                                      selections: [
                                        {
                                          kind: "Field",
                                          name: { kind: "Name", value: "sys" },
                                          selectionSet: {
                                            kind: "SelectionSet",
                                            selections: [
                                              {
                                                kind: "Field",
                                                name: {
                                                  kind: "Name",
                                                  value: "id",
                                                },
                                              },
                                            ],
                                          },
                                        },
                                        {
                                          kind: "Field",
                                          name: { kind: "Name", value: "name" },
                                        },
                                        {
                                          kind: "Field",
                                          name: {
                                            kind: "Name",
                                            value: "isRootCategory",
                                          },
                                        },
                                        {
                                          kind: "Field",
                                          name: {
                                            kind: "Name",
                                            value: "displayName",
                                          },
                                        },
                                        {
                                          kind: "Field",
                                          name: { kind: "Name", value: "slug" },
                                        },
                                      ],
                                    },
                                  },
                                ],
                              },
                            },
                          ],
                        },
                      },
                    ],
                  },
                },
              ],
            },
          },
        ],
      },
    },
  ],
} as unknown as DocumentNode<
  FetchCategoriesQuery,
  FetchCategoriesQueryVariables
>;
export const FetchCategoryAttributesDocument = {
  kind: "Document",
  definitions: [
    {
      kind: "OperationDefinition",
      operation: "query",
      name: { kind: "Name", value: "FetchCategoryAttributes" },
      variableDefinitions: [
        {
          kind: "VariableDefinition",
          variable: {
            kind: "Variable",
            name: { kind: "Name", value: "categorySlug" },
          },
          type: {
            kind: "NonNullType",
            type: {
              kind: "NamedType",
              name: { kind: "Name", value: "String" },
            },
          },
        },
      ],
      selectionSet: {
        kind: "SelectionSet",
        selections: [
          {
            kind: "Field",
            name: { kind: "Name", value: "categoryCollection" },
            arguments: [
              {
                kind: "Argument",
                name: { kind: "Name", value: "where" },
                value: {
                  kind: "ObjectValue",
                  fields: [
                    {
                      kind: "ObjectField",
                      name: { kind: "Name", value: "slug" },
                      value: {
                        kind: "Variable",
                        name: { kind: "Name", value: "categorySlug" },
                      },
                    },
                  ],
                },
              },
            ],
            selectionSet: {
              kind: "SelectionSet",
              selections: [
                {
                  kind: "Field",
                  name: { kind: "Name", value: "items" },
                  selectionSet: {
                    kind: "SelectionSet",
                    selections: [
                      {
                        kind: "Field",
                        name: {
                          kind: "Name",
                          value: "unionAttributesCollection",
                        },
                        arguments: [
                          {
                            kind: "Argument",
                            name: { kind: "Name", value: "limit" },
                            value: { kind: "IntValue", value: "20" },
                          },
                        ],
                        selectionSet: {
                          kind: "SelectionSet",
                          selections: [
                            {
                              kind: "Field",
                              name: { kind: "Name", value: "items" },
                              selectionSet: {
                                kind: "SelectionSet",
                                selections: [
                                  {
                                    kind: "Field",
                                    name: { kind: "Name", value: "slug" },
                                  },
                                  {
                                    kind: "Field",
                                    name: { kind: "Name", value: "sys" },
                                    selectionSet: {
                                      kind: "SelectionSet",
                                      selections: [
                                        {
                                          kind: "Field",
                                          name: { kind: "Name", value: "id" },
                                        },
                                      ],
                                    },
                                  },
                                ],
                              },
                            },
                          ],
                        },
                      },
                      {
                        kind: "Field",
                        name: {
                          kind: "Name",
                          value: "intersectAttributesCollection",
                        },
                        arguments: [
                          {
                            kind: "Argument",
                            name: { kind: "Name", value: "limit" },
                            value: { kind: "IntValue", value: "20" },
                          },
                        ],
                        selectionSet: {
                          kind: "SelectionSet",
                          selections: [
                            {
                              kind: "Field",
                              name: { kind: "Name", value: "items" },
                              selectionSet: {
                                kind: "SelectionSet",
                                selections: [
                                  {
                                    kind: "Field",
                                    name: { kind: "Name", value: "sys" },
                                    selectionSet: {
                                      kind: "SelectionSet",
                                      selections: [
                                        {
                                          kind: "Field",
                                          name: { kind: "Name", value: "id" },
                                        },
                                      ],
                                    },
                                  },
                                  {
                                    kind: "Field",
                                    name: { kind: "Name", value: "slug" },
                                  },
                                ],
                              },
                            },
                          ],
                        },
                      },
                    ],
                  },
                },
              ],
            },
          },
        ],
      },
    },
  ],
} as unknown as DocumentNode<
  FetchCategoryAttributesQuery,
  FetchCategoryAttributesQueryVariables
>;
export const FetchCategoryHighlightsDocument = {
  kind: "Document",
  definitions: [
    {
      kind: "OperationDefinition",
      operation: "query",
      name: { kind: "Name", value: "FetchCategoryHighlights" },
      selectionSet: {
        kind: "SelectionSet",
        selections: [
          {
            kind: "Field",
            name: { kind: "Name", value: "categoryHighlightCollection" },
            arguments: [
              {
                kind: "Argument",
                name: { kind: "Name", value: "limit" },
                value: { kind: "IntValue", value: "3" },
              },
            ],
            selectionSet: {
              kind: "SelectionSet",
              selections: [
                {
                  kind: "Field",
                  name: { kind: "Name", value: "items" },
                  selectionSet: {
                    kind: "SelectionSet",
                    selections: [
                      {
                        kind: "Field",
                        name: { kind: "Name", value: "category" },
                        selectionSet: {
                          kind: "SelectionSet",
                          selections: [
                            {
                              kind: "Field",
                              name: { kind: "Name", value: "slug" },
                            },
                          ],
                        },
                      },
                      {
                        kind: "Field",
                        name: {
                          kind: "Name",
                          value: "highlightSlidesCollection",
                        },
                        arguments: [
                          {
                            kind: "Argument",
                            name: { kind: "Name", value: "limit" },
                            value: { kind: "IntValue", value: "10" },
                          },
                        ],
                        selectionSet: {
                          kind: "SelectionSet",
                          selections: [
                            {
                              kind: "Field",
                              name: { kind: "Name", value: "items" },
                              selectionSet: {
                                kind: "SelectionSet",
                                selections: [
                                  {
                                    kind: "Field",
                                    name: { kind: "Name", value: "theme" },
                                  },
                                  {
                                    kind: "Field",
                                    name: { kind: "Name", value: "media" },
                                    selectionSet: {
                                      kind: "SelectionSet",
                                      selections: [
                                        {
                                          kind: "Field",
                                          name: { kind: "Name", value: "url" },
                                        },
                                      ],
                                    },
                                  },
                                  {
                                    kind: "Field",
                                    name: { kind: "Name", value: "category" },
                                    selectionSet: {
                                      kind: "SelectionSet",
                                      selections: [
                                        {
                                          kind: "Field",
                                          name: { kind: "Name", value: "slug" },
                                        },
                                        {
                                          kind: "Field",
                                          name: {
                                            kind: "Name",
                                            value: "displayName",
                                          },
                                        },
                                      ],
                                    },
                                  },
                                ],
                              },
                            },
                          ],
                        },
                      },
                    ],
                  },
                },
              ],
            },
          },
        ],
      },
    },
  ],
} as unknown as DocumentNode<
  FetchCategoryHighlightsQuery,
  FetchCategoryHighlightsQueryVariables
>;
export const FetchProductDocument = {
  kind: "Document",
  definitions: [
    {
      kind: "OperationDefinition",
      operation: "query",
      name: { kind: "Name", value: "FetchProduct" },
      variableDefinitions: [
        {
          kind: "VariableDefinition",
          variable: {
            kind: "Variable",
            name: { kind: "Name", value: "productSlug" },
          },
          type: {
            kind: "NonNullType",
            type: {
              kind: "NamedType",
              name: { kind: "Name", value: "String" },
            },
          },
        },
      ],
      selectionSet: {
        kind: "SelectionSet",
        selections: [
          {
            kind: "Field",
            name: { kind: "Name", value: "productCollection" },
            arguments: [
              {
                kind: "Argument",
                name: { kind: "Name", value: "where" },
                value: {
                  kind: "ObjectValue",
                  fields: [
                    {
                      kind: "ObjectField",
                      name: { kind: "Name", value: "slug" },
                      value: {
                        kind: "Variable",
                        name: { kind: "Name", value: "productSlug" },
                      },
                    },
                  ],
                },
              },
              {
                kind: "Argument",
                name: { kind: "Name", value: "limit" },
                value: { kind: "IntValue", value: "1" },
              },
            ],
            selectionSet: {
              kind: "SelectionSet",
              selections: [
                {
                  kind: "Field",
                  name: { kind: "Name", value: "items" },
                  selectionSet: {
                    kind: "SelectionSet",
                    selections: [
                      { kind: "Field", name: { kind: "Name", value: "name" } },
                      {
                        kind: "Field",
                        name: { kind: "Name", value: "description" },
                      },
                      { kind: "Field", name: { kind: "Name", value: "slug" } },
                      {
                        kind: "Field",
                        name: { kind: "Name", value: "variantsCollection" },
                        arguments: [
                          {
                            kind: "Argument",
                            name: { kind: "Name", value: "limit" },
                            value: { kind: "IntValue", value: "20" },
                          },
                        ],
                        selectionSet: {
                          kind: "SelectionSet",
                          selections: [
                            {
                              kind: "Field",
                              name: { kind: "Name", value: "items" },
                              selectionSet: {
                                kind: "SelectionSet",
                                selections: [
                                  {
                                    kind: "Field",
                                    name: { kind: "Name", value: "ref" },
                                  },
                                  {
                                    kind: "Field",
                                    name: { kind: "Name", value: "colorName" },
                                  },
                                  {
                                    kind: "Field",
                                    name: { kind: "Name", value: "colorCode" },
                                  },
                                  {
                                    kind: "Field",
                                    name: { kind: "Name", value: "price" },
                                  },
                                  {
                                    kind: "Field",
                                    name: { kind: "Name", value: "skuList" },
                                  },
                                  {
                                    kind: "Field",
                                    name: {
                                      kind: "Name",
                                      value: "firstMediaInOverview",
                                    },
                                  },
                                  {
                                    kind: "Field",
                                    name: {
                                      kind: "Name",
                                      value: "attributesCollection",
                                    },
                                    selectionSet: {
                                      kind: "SelectionSet",
                                      selections: [
                                        {
                                          kind: "Field",
                                          name: {
                                            kind: "Name",
                                            value: "items",
                                          },
                                          selectionSet: {
                                            kind: "SelectionSet",
                                            selections: [
                                              {
                                                kind: "Field",
                                                name: {
                                                  kind: "Name",
                                                  value: "slug",
                                                },
                                              },
                                              {
                                                kind: "Field",
                                                name: {
                                                  kind: "Name",
                                                  value: "name",
                                                },
                                              },
                                            ],
                                          },
                                        },
                                      ],
                                    },
                                  },
                                  {
                                    kind: "Field",
                                    name: {
                                      kind: "Name",
                                      value: "mediaCollection",
                                    },
                                    selectionSet: {
                                      kind: "SelectionSet",
                                      selections: [
                                        {
                                          kind: "Field",
                                          name: {
                                            kind: "Name",
                                            value: "items",
                                          },
                                          selectionSet: {
                                            kind: "SelectionSet",
                                            selections: [
                                              {
                                                kind: "Field",
                                                name: {
                                                  kind: "Name",
                                                  value: "url",
                                                },
                                              },
                                            ],
                                          },
                                        },
                                      ],
                                    },
                                  },
                                ],
                              },
                            },
                          ],
                        },
                      },
                    ],
                  },
                },
              ],
            },
          },
        ],
      },
    },
  ],
} as unknown as DocumentNode<FetchProductQuery, FetchProductQueryVariables>;
export const FetchProductVariantsInCategoryDocument = {
  kind: "Document",
  definitions: [
    {
      kind: "OperationDefinition",
      operation: "query",
      name: { kind: "Name", value: "FetchProductVariantsInCategory" },
      variableDefinitions: [
        {
          kind: "VariableDefinition",
          variable: {
            kind: "Variable",
            name: { kind: "Name", value: "intersectCondition" },
          },
          type: {
            kind: "ListType",
            type: {
              kind: "NonNullType",
              type: {
                kind: "NamedType",
                name: { kind: "Name", value: "ProductVariantFilter" },
              },
            },
          },
        },
        {
          kind: "VariableDefinition",
          variable: {
            kind: "Variable",
            name: { kind: "Name", value: "unionCondition" },
          },
          type: {
            kind: "ListType",
            type: {
              kind: "NonNullType",
              type: {
                kind: "NamedType",
                name: { kind: "Name", value: "ProductVariantFilter" },
              },
            },
          },
        },
      ],
      selectionSet: {
        kind: "SelectionSet",
        selections: [
          {
            kind: "Field",
            name: { kind: "Name", value: "productVariantCollection" },
            arguments: [
              {
                kind: "Argument",
                name: { kind: "Name", value: "where" },
                value: {
                  kind: "ObjectValue",
                  fields: [
                    {
                      kind: "ObjectField",
                      name: { kind: "Name", value: "AND" },
                      value: {
                        kind: "Variable",
                        name: { kind: "Name", value: "intersectCondition" },
                      },
                    },
                    {
                      kind: "ObjectField",
                      name: { kind: "Name", value: "OR" },
                      value: {
                        kind: "Variable",
                        name: { kind: "Name", value: "unionCondition" },
                      },
                    },
                  ],
                },
              },
            ],
            selectionSet: {
              kind: "SelectionSet",
              selections: [
                {
                  kind: "Field",
                  name: { kind: "Name", value: "items" },
                  selectionSet: {
                    kind: "SelectionSet",
                    selections: [
                      { kind: "Field", name: { kind: "Name", value: "ref" } },
                      { kind: "Field", name: { kind: "Name", value: "price" } },
                      {
                        kind: "Field",
                        name: { kind: "Name", value: "firstMediaInOverview" },
                      },
                      {
                        kind: "Field",
                        name: { kind: "Name", value: "linkedFrom" },
                        selectionSet: {
                          kind: "SelectionSet",
                          selections: [
                            {
                              kind: "Field",
                              name: {
                                kind: "Name",
                                value: "productCollection",
                              },
                              arguments: [
                                {
                                  kind: "Argument",
                                  name: { kind: "Name", value: "limit" },
                                  value: { kind: "IntValue", value: "1" },
                                },
                              ],
                              selectionSet: {
                                kind: "SelectionSet",
                                selections: [
                                  {
                                    kind: "Field",
                                    name: { kind: "Name", value: "items" },
                                    selectionSet: {
                                      kind: "SelectionSet",
                                      selections: [
                                        {
                                          kind: "Field",
                                          name: { kind: "Name", value: "slug" },
                                        },
                                        {
                                          kind: "Field",
                                          name: { kind: "Name", value: "name" },
                                        },
                                        {
                                          kind: "Field",
                                          name: {
                                            kind: "Name",
                                            value: "variantsCollection",
                                          },
                                          arguments: [
                                            {
                                              kind: "Argument",
                                              name: {
                                                kind: "Name",
                                                value: "limit",
                                              },
                                              value: {
                                                kind: "IntValue",
                                                value: "0",
                                              },
                                            },
                                          ],
                                          selectionSet: {
                                            kind: "SelectionSet",
                                            selections: [
                                              {
                                                kind: "Field",
                                                name: {
                                                  kind: "Name",
                                                  value: "total",
                                                },
                                              },
                                            ],
                                          },
                                        },
                                      ],
                                    },
                                  },
                                ],
                              },
                            },
                          ],
                        },
                      },
                      {
                        kind: "Field",
                        name: { kind: "Name", value: "attributesCollection" },
                        arguments: [
                          {
                            kind: "Argument",
                            name: { kind: "Name", value: "limit" },
                            value: { kind: "IntValue", value: "10" },
                          },
                        ],
                        selectionSet: {
                          kind: "SelectionSet",
                          selections: [
                            {
                              kind: "Field",
                              name: { kind: "Name", value: "items" },
                              selectionSet: {
                                kind: "SelectionSet",
                                selections: [
                                  {
                                    kind: "Field",
                                    name: { kind: "Name", value: "slug" },
                                  },
                                  {
                                    kind: "Field",
                                    name: { kind: "Name", value: "type" },
                                  },
                                  {
                                    kind: "Field",
                                    name: { kind: "Name", value: "name" },
                                  },
                                ],
                              },
                            },
                          ],
                        },
                      },
                      {
                        kind: "Field",
                        name: { kind: "Name", value: "mediaCollection" },
                        arguments: [
                          {
                            kind: "Argument",
                            name: { kind: "Name", value: "limit" },
                            value: { kind: "IntValue", value: "15" },
                          },
                        ],
                        selectionSet: {
                          kind: "SelectionSet",
                          selections: [
                            {
                              kind: "Field",
                              name: { kind: "Name", value: "items" },
                              selectionSet: {
                                kind: "SelectionSet",
                                selections: [
                                  {
                                    kind: "Field",
                                    name: { kind: "Name", value: "url" },
                                  },
                                ],
                              },
                            },
                          ],
                        },
                      },
                      {
                        kind: "Field",
                        name: { kind: "Name", value: "skuList" },
                      },
                    ],
                  },
                },
              ],
            },
          },
        ],
      },
    },
  ],
} as unknown as DocumentNode<
  FetchProductVariantsInCategoryQuery,
  FetchProductVariantsInCategoryQueryVariables
>;
