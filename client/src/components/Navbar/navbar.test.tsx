import React from "react";
import { render, screen } from "@testing-library/react";
import { Navbar } from ".";

describe("Navbar Component", () => {
  test("it contains a link that points to the homepage", () => {
    render(<Navbar />);
    const linkElement = screen.getByRole("link", { name: /lavish-logo/i });
    expect(linkElement).toHaveAttribute("href", "/");
  });
});
