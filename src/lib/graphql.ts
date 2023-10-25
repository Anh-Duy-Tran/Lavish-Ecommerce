import { cacheExchange, createClient, fetchExchange } from "@urql/core";
import { registerUrql } from "@urql/next/rsc";

const makeClient = () => {
  return createClient({
    url: `https://graphql.contentful.com/content/v1/spaces/${process.env.CONTENTFUL_SPACE_ID}`,
    exchanges: [cacheExchange, fetchExchange],
    fetchOptions: {
      cache: "no-store",
      headers: {
        authorization: `Bearer ${process.env.CONTENTFUL_ACCESS_TOKEN}`,
      },
    },
  });
};

export const { getClient } = registerUrql(makeClient);
