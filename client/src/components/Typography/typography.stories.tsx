import React from "react";

import type { Meta, StoryFn, StoryObj } from "@storybook/react";
import { Typography } from ".";

const meta = {
  title: "Components/Typography",
  component: Typography,
  parameters: {
    layout: "centered",
  },
  tags: ["autodocs"],
  argTypes: {},
} satisfies Meta<typeof Typography>;

export default meta;
type Story = StoryObj<typeof meta>;

const Template: StoryFn<typeof Typography> = (args) => <Typography {...args} />;

export const Primary = Template.bind({});
Primary.args = {
  children: "Hello, world!",
  variant: "heading",
};
