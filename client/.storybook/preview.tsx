import React from "react";
import { Decorator, type Preview } from "@storybook/react";
import { PaletteProvider } from "../src/theme/usePalette";

const preview: Preview = {
  parameters: {
    actions: { argTypesRegex: "^on[A-Z].*" },
    controls: {
      matchers: {
        color: /(background|color)$/i,
        date: /Date$/,
      },
    },
  },
  globalTypes: {
    theme: {
      description: "Global theme for components",
      defaultValue: "light",
      toolbar: {
        title: "Theme",
        icon: "mirror",
        items: ["light", "dark"],
        dynamicTitle: true,
      },
    },
  },
};

export const WithColorScheme: Decorator = (Story, context) => {
  let mode = context.globals.theme;

  return (
    <PaletteProvider modeProps={mode}>
      <Story />
    </PaletteProvider>
  );
};

export const decorators = [WithColorScheme];

export default preview;
