export interface Palette {
  background: string;
  text: string;
  primary: string;
  secondary: string;
}

export const lightPalette: Palette = {
  background: "#ffffff",
  text: "#000000",
  primary: "#990000",
  secondary: "#d3455b",
};

export const darkPalette: Palette = {
  background: "#000000",
  text: "#ffffff",
  primary: "#000099",
  secondary: "#ff6978",
};
