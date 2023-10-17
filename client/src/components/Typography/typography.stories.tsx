import React from "react";

import type { Meta, StoryFn } from "@storybook/react";
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
// type Story = StoryObj<typeof meta>;

const Template: StoryFn<typeof Typography> = (args) => <Typography {...args} />;

export const Heading = Template.bind({});
Heading.args = {
  children: "Heading: Hello, world!",
  variant: "heading",
};

export const Text = Template.bind({});
Text.args = {
  children: "Text: Hello, world!",
  variant: "text",
};

export const Subtitle = Template.bind({});
Subtitle.args = {
  children: "Subtitle: Hello, world!",
  variant: "subtitle",
};
