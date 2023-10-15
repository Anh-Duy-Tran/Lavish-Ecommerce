import type { StorybookConfig } from "@storybook/nextjs";
import path from "path";

const config: StorybookConfig = {
  stories: ["../src/**/*.mdx", "../src/**/*.stories.@(js|jsx|mjs|ts|tsx)"],
  addons: [
    "@storybook/addon-links",
    "@storybook/addon-essentials",
    "@storybook/addon-onboarding",
    "@storybook/addon-interactions",
  ],
  framework: {
    name: "@storybook/nextjs",
    options: {},
  },
  docs: {
    autodocs: "tag",
  },
  webpackFinal: async (config, _) => {
    config.resolve!.modules = [path.resolve(__dirname, ".."), "node_modules"];
    config.resolve!.alias = {
      ...config.resolve!.alias,
      "@": path.resolve(__dirname, "../src"),
      "next/image": path.resolve(__dirname, "./mocks/NextImageMock.js"),
    };
    return config;
  },
};
export default config;
