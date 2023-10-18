import React from "react";
import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import "@testing-library/jest-dom";
import { Button } from ".";
import { usePalette } from "@/theme/usePalette";
import { lightPalette } from "@/theme/palettes";

jest.mock("@/theme/usePalette", () => ({
  usePalette: jest.fn(),
}));

describe("StyledButton Component", () => {
  beforeEach(() => {
    // Reset the mock implementation before each test
    jest.mocked(usePalette).mockImplementation(() => lightPalette);
  });

  it("renders correctly", () => {
    const { asFragment } = render(
      <>
        <Button variant="contained">Snapshot1</Button>
        <Button variant="outlined">Snapshot1</Button>
        <Button variant="text">Snapshot1</Button>
      </>,
    );
    expect(asFragment()).toMatchSnapshot();
  });

  it("renders label content correctly", () => {
    render(<Button>Click me</Button>);
    expect(screen.getByText("Click me"));
  });

  it("handles click event", async () => {
    const handleClick = jest.fn();
    render(<Button onClick={handleClick}>Click me</Button>);
    await userEvent.click(screen.getByText("Click me"));
    expect(handleClick).toHaveBeenCalledTimes(1);
  });

  it("occupies all available space when fullWidth prop is true", () => {
    render(<Button fullWidth>Click me</Button>);
    expect(screen.getByRole("button")).toHaveClass("w-full");
  });
});
