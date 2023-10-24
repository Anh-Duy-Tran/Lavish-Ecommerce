import React from "react";
import type { Meta, StoryFn } from "@storybook/react";
import { Navbar } from ".";

const meta = {
  title: "Components/Navbar",
  component: Navbar,
  argTypes: {},
} satisfies Meta<typeof Navbar>;

export default meta;

const Template: StoryFn<typeof Navbar> = () => <Navbar />;

export const Primary = Template.bind({});
Primary.args = {};
