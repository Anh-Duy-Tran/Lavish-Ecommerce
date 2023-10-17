import React from "react";
import { Decorator, type Preview } from "@storybook/react";
import { PaletteProvider } from "../src/theme/usePalette";
import styled from "@emotion/styled";

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
        items: ["light", "dark", "side-by-side"],
        dynamicTitle: true,
      },
    },
  },
};

const ThemeBlock = styled.div<{ left?: boolean; fill?: boolean }>(
  ({ left, fill, theme }) =>
    `
      position: absolute;
      top: 0;
      left: ${left || fill ? 0 : "50vw"};
      border-right: ${left ? "1px solid #202020" : "none"};
      right: ${left ? "50vw" : 0};
      width: ${fill ? "100vw" : "50vw"};
      height: 100vh;
      bottom: 0;
      overflow: auto;
      display: flex;
      justify-content: center;
      align-items: center;
      background-color: ${theme};
    `,
);

export const WithColorScheme: Decorator = (Story, context) => {
  let mode = context.globals.theme;

  if (mode === "side-by-side") {
    return (
      <div style={{ display: "flex" }}>
        <PaletteProvider modeProps={"light"}>
          <ThemeBlock left theme={"white"}>
            <Story />
          </ThemeBlock>
        </PaletteProvider>
        <PaletteProvider modeProps={"dark"}>
          <ThemeBlock theme={"black"}>
            <Story />
          </ThemeBlock>
        </PaletteProvider>
      </div>
    );
  }

  return (
    <PaletteProvider modeProps={mode}>
      <Story />
    </PaletteProvider>
  );
};

export const decorators = [WithColorScheme];

export default preview;
