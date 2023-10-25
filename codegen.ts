import { CodegenConfig } from "@graphql-codegen/cli";
import "dotenv/config";

const config: CodegenConfig = {
  schema: [
    {
      [`https://graphql.contentful.com/content/v1/spaces/${process.env.CONTENTFUL_SPACE_ID}`]:
        {
          headers: {
            Authorization: `Bearer ${process.env.CONTENTFUL_ACCESS_TOKEN}`,
          },
        },
    },
  ],

  config: {
    nonOptionalTypename: false,
  },

  documents: ["src/graphql/*.graphql"],
  ignoreNoDocuments: true, // for better experience with the watcher
  generates: {
    "./src/gql/": {
      preset: "client",
    },
  },
};

export default config;
