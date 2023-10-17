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
        <Button variant="contained" label="Snapshot1" />
        <Button variant="outlined" label="Snapshot2" />
        <Button variant="text" label="Snapshot3" />
      </>,
    );
    expect(asFragment()).toMatchSnapshot();
  });

  it("renders label content correctly", () => {
    render(<Button label="Click me" />);
    expect(screen.getByText("Click me"));
  });

  it("renders children when passed", () => {
    render(<Button>Children</Button>);
    expect(screen.getByText("Children")).toBeInTheDocument();
  });

  it("renders label over children when both are passed", () => {
    render(<Button label="Label">Children</Button>);
    expect(screen.getByText("Label")).toBeInTheDocument();
    expect(screen.queryByText("Children")).not.toBeInTheDocument();
  });

  it("handles click event", async () => {
    const handleClick = jest.fn();
    render(<Button onClick={handleClick} label="Click me" />);
    await userEvent.click(screen.getByText("Click me"));
    expect(handleClick).toHaveBeenCalledTimes(1);
  });

  it("applies the correct width when the width prop is provided", () => {
    render(<Button width={300} label="Click me" />);
    expect(screen.getByRole("button")).toHaveStyle("width: 300px");
  });

  it("occupies all available space when fullWidth prop is true", () => {
    render(<Button fullWidth label="Click me" />);
    expect(screen.getByRole("button")).toHaveStyle("width: 100%");
  });
});
