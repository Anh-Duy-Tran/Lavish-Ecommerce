import React from "react";
import { render } from "@testing-library/react";
import { Typography } from ".";

describe("Typography component", () => {
  it("renders correctly", () => {
    const { asFragment } = render(
      <>
        <Typography variant="heading">Test Content</Typography>
        <Typography variant="text">Test Content</Typography>
        <Typography variant="subtitle">Test Content</Typography>
      </>
    );
    expect(asFragment()).toMatchSnapshot();
  });

  it("renders children content", () => {
    const { getByText } = render(
      <Typography variant="text">Test Content</Typography>
    );
    expect(getByText("Test Content")).toBeInTheDocument();
  });

  it('applies bold styling when "bold" prop is provided', () => {
    const { getByText } = render(
      <Typography variant="text" bold>
        Bold Text
      </Typography>
    );
    expect(getByText("Bold Text")).toHaveStyle("font-weight: 700");
  });

  it('applies compact styling when "compact" prop is provided', () => {
    const { getByText } = render(
      <Typography variant="text" compact>
        Compact Text
      </Typography>
    );
    expect(getByText("Compact Text")).toHaveStyle("margin: 0px");
  });

  it("renders with correct font-size based on variant", () => {
    const { getByText, rerender } = render(
      <Typography variant="heading">Heading</Typography>
    );
    expect(getByText("Heading")).toHaveStyle("font-size: 13px");

    rerender(<Typography variant="text">Text</Typography>);
    expect(getByText("Text")).toHaveStyle("font-size: 13px");
  });
});
