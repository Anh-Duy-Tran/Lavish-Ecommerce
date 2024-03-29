/* eslint-disable */
import * as types from "./graphql";
import { TypedDocumentNode as DocumentNode } from "@graphql-typed-document-node/core";

/**
 * Map of all GraphQL operations in the project.
 *
 * This map has several performance disadvantages:
 * 1. It is not tree-shakeable, so it will include all operations in the project.
 * 2. It is not minifiable, so the string of a GraphQL query will be multiple times inside the bundle.
 * 3. It does not support dead code elimination, so it will add unused operations.
 *
 * Therefore it is highly recommended to use the babel or swc plugin for production.
 */
const documents = {
  'query FetchCategories($lang: String!) {\n  categories(id: "1Dxj0jPKVb5TgkZ2RYRp7x", locale: $lang) {\n    categoriesCollection(limit: 3) {\n      items {\n        sys {\n          id\n        }\n        name\n        isRootCategory\n        displayName\n        slug\n        subCategoriesCollection {\n          items {\n            sys {\n              id\n            }\n            name\n            isRootCategory\n            displayName\n            slug\n          }\n        }\n      }\n    }\n  }\n}':
    types.FetchCategoriesDocument,
  "query FetchCategoryAttributes($categorySlug: String!) {\n  categoryCollection(where: {slug: $categorySlug}) {\n    items {\n      unionAttributesCollection(limit: 20) {\n        items {\n          slug\n          sys {\n            id\n          }\n        }\n      }\n      intersectAttributesCollection(limit: 20) {\n        items {\n          sys {\n            id\n          }\n          slug\n        }\n      }\n    }\n  }\n}":
    types.FetchCategoryAttributesDocument,
  "query FetchCategoryHighlights {\n  categoryHighlightCollection(limit: 3) {\n    items {\n      category {\n        slug\n      }\n      highlightSlidesCollection(limit: 10) {\n        items {\n          theme\n          media {\n            url\n          }\n          category {\n            slug\n            displayName\n          }\n        }\n      }\n    }\n  }\n}":
    types.FetchCategoryHighlightsDocument,
  "query FetchProduct($productSlug: String!) {\n  productCollection(where: {slug: $productSlug}, limit: 1) {\n    items {\n      name\n      description\n      slug\n      variantsCollection(limit: 20) {\n        items {\n          ref\n          colorName\n          colorCode\n          price\n          skuList\n          firstMediaInOverview\n          attributesCollection {\n            items {\n              slug\n              name\n            }\n          }\n          mediaCollection {\n            items {\n              url\n            }\n          }\n        }\n      }\n    }\n  }\n}":
    types.FetchProductDocument,
  "query FetchProductVariantsInCategory($intersectCondition: [ProductVariantFilter!], $unionCondition: [ProductVariantFilter!]) {\n  productVariantCollection(where: {AND: $intersectCondition, OR: $unionCondition}) {\n    items {\n      ref\n      price\n      firstMediaInOverview\n      colorName\n      linkedFrom {\n        productCollection(limit: 1) {\n          items {\n            slug\n            name\n            variantsCollection(limit: 0) {\n              total\n            }\n          }\n        }\n      }\n      attributesCollection(limit: 10) {\n        items {\n          slug\n          type\n          name\n        }\n      }\n      mediaCollection(limit: 15) {\n        items {\n          url\n        }\n      }\n      skuList\n    }\n  }\n}":
    types.FetchProductVariantsInCategoryDocument,
};

/**
 * The graphql function is used to parse GraphQL queries into a document that can be used by GraphQL clients.
 *
 *
 * @example
 * ```ts
 * const query = graphql(`query GetUser($id: ID!) { user(id: $id) { name } }`);
 * ```
 *
 * The query argument is unknown!
 * Please regenerate the types.
 */
export function graphql(source: string): unknown;

/**
 * The graphql function is used to parse GraphQL queries into a document that can be used by GraphQL clients.
 */
export function graphql(
  source: 'query FetchCategories($lang: String!) {\n  categories(id: "1Dxj0jPKVb5TgkZ2RYRp7x", locale: $lang) {\n    categoriesCollection(limit: 3) {\n      items {\n        sys {\n          id\n        }\n        name\n        isRootCategory\n        displayName\n        slug\n        subCategoriesCollection {\n          items {\n            sys {\n              id\n            }\n            name\n            isRootCategory\n            displayName\n            slug\n          }\n        }\n      }\n    }\n  }\n}',
): (typeof documents)['query FetchCategories($lang: String!) {\n  categories(id: "1Dxj0jPKVb5TgkZ2RYRp7x", locale: $lang) {\n    categoriesCollection(limit: 3) {\n      items {\n        sys {\n          id\n        }\n        name\n        isRootCategory\n        displayName\n        slug\n        subCategoriesCollection {\n          items {\n            sys {\n              id\n            }\n            name\n            isRootCategory\n            displayName\n            slug\n          }\n        }\n      }\n    }\n  }\n}'];
/**
 * The graphql function is used to parse GraphQL queries into a document that can be used by GraphQL clients.
 */
export function graphql(
  source: "query FetchCategoryAttributes($categorySlug: String!) {\n  categoryCollection(where: {slug: $categorySlug}) {\n    items {\n      unionAttributesCollection(limit: 20) {\n        items {\n          slug\n          sys {\n            id\n          }\n        }\n      }\n      intersectAttributesCollection(limit: 20) {\n        items {\n          sys {\n            id\n          }\n          slug\n        }\n      }\n    }\n  }\n}",
): (typeof documents)["query FetchCategoryAttributes($categorySlug: String!) {\n  categoryCollection(where: {slug: $categorySlug}) {\n    items {\n      unionAttributesCollection(limit: 20) {\n        items {\n          slug\n          sys {\n            id\n          }\n        }\n      }\n      intersectAttributesCollection(limit: 20) {\n        items {\n          sys {\n            id\n          }\n          slug\n        }\n      }\n    }\n  }\n}"];
/**
 * The graphql function is used to parse GraphQL queries into a document that can be used by GraphQL clients.
 */
export function graphql(
  source: "query FetchCategoryHighlights {\n  categoryHighlightCollection(limit: 3) {\n    items {\n      category {\n        slug\n      }\n      highlightSlidesCollection(limit: 10) {\n        items {\n          theme\n          media {\n            url\n          }\n          category {\n            slug\n            displayName\n          }\n        }\n      }\n    }\n  }\n}",
): (typeof documents)["query FetchCategoryHighlights {\n  categoryHighlightCollection(limit: 3) {\n    items {\n      category {\n        slug\n      }\n      highlightSlidesCollection(limit: 10) {\n        items {\n          theme\n          media {\n            url\n          }\n          category {\n            slug\n            displayName\n          }\n        }\n      }\n    }\n  }\n}"];
/**
 * The graphql function is used to parse GraphQL queries into a document that can be used by GraphQL clients.
 */
export function graphql(
  source: "query FetchProduct($productSlug: String!) {\n  productCollection(where: {slug: $productSlug}, limit: 1) {\n    items {\n      name\n      description\n      slug\n      variantsCollection(limit: 20) {\n        items {\n          ref\n          colorName\n          colorCode\n          price\n          skuList\n          firstMediaInOverview\n          attributesCollection {\n            items {\n              slug\n              name\n            }\n          }\n          mediaCollection {\n            items {\n              url\n            }\n          }\n        }\n      }\n    }\n  }\n}",
): (typeof documents)["query FetchProduct($productSlug: String!) {\n  productCollection(where: {slug: $productSlug}, limit: 1) {\n    items {\n      name\n      description\n      slug\n      variantsCollection(limit: 20) {\n        items {\n          ref\n          colorName\n          colorCode\n          price\n          skuList\n          firstMediaInOverview\n          attributesCollection {\n            items {\n              slug\n              name\n            }\n          }\n          mediaCollection {\n            items {\n              url\n            }\n          }\n        }\n      }\n    }\n  }\n}"];
/**
 * The graphql function is used to parse GraphQL queries into a document that can be used by GraphQL clients.
 */
export function graphql(
  source: "query FetchProductVariantsInCategory($intersectCondition: [ProductVariantFilter!], $unionCondition: [ProductVariantFilter!]) {\n  productVariantCollection(where: {AND: $intersectCondition, OR: $unionCondition}) {\n    items {\n      ref\n      price\n      firstMediaInOverview\n      colorName\n      linkedFrom {\n        productCollection(limit: 1) {\n          items {\n            slug\n            name\n            variantsCollection(limit: 0) {\n              total\n            }\n          }\n        }\n      }\n      attributesCollection(limit: 10) {\n        items {\n          slug\n          type\n          name\n        }\n      }\n      mediaCollection(limit: 15) {\n        items {\n          url\n        }\n      }\n      skuList\n    }\n  }\n}",
): (typeof documents)["query FetchProductVariantsInCategory($intersectCondition: [ProductVariantFilter!], $unionCondition: [ProductVariantFilter!]) {\n  productVariantCollection(where: {AND: $intersectCondition, OR: $unionCondition}) {\n    items {\n      ref\n      price\n      firstMediaInOverview\n      colorName\n      linkedFrom {\n        productCollection(limit: 1) {\n          items {\n            slug\n            name\n            variantsCollection(limit: 0) {\n              total\n            }\n          }\n        }\n      }\n      attributesCollection(limit: 10) {\n        items {\n          slug\n          type\n          name\n        }\n      }\n      mediaCollection(limit: 15) {\n        items {\n          url\n        }\n      }\n      skuList\n    }\n  }\n}"];

export function graphql(source: string) {
  return (documents as any)[source] ?? {};
}

export type DocumentType<TDocumentNode extends DocumentNode<any, any>> =
  TDocumentNode extends DocumentNode<infer TType, any> ? TType : never;
