import { render, screen } from "@testing-library/react";
import { Button } from ".";

describe("Button", () => {
  it("should run this test", () => {
    render(<Button />);
    expect(true).toBe(true);
  });
});
