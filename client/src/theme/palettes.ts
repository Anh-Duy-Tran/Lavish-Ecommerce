type PaletteElement = {
  background: string;
  text: string;
};

export interface Palette {
  primary: PaletteElement;
  secondary: PaletteElement;
}

export const lightPalette: Palette = {
  primary: {
    background: "#FFFFFF",
    text: "#000000",
  },
  secondary: {
    background: "#DDDDDD",
    text: "#222222",
  },
};

export const darkPalette: Palette = {
  primary: {
    background: "#000000",
    text: "#FFFFFF",
  },
  secondary: {
    text: "#DDDDDD",
    background: "#222222",
  },
};
