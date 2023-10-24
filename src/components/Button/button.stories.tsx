import React, { useState } from "react";
import type { Meta, StoryFn, StoryObj } from "@storybook/react";
import { Button, ButtonProps } from "./Button";

const meta = {
  title: "Components/Button",
  component: Button,
  parameters: {
    layout: "centered",
  },
  tags: ["autodocs"],
  argTypes: {},
} satisfies Meta<typeof Button>;

export default meta;
type Story = StoryObj<typeof meta>;

const ToggleableButton = ({
  active,
  setActive,
  ...props
}: ButtonProps & {
  active: boolean;
  setActive: React.Dispatch<React.SetStateAction<boolean>>;
}) => {
  return (
    <Button
      {...props}
      active={active}
      onClick={() => setActive((prev) => !prev)}
    />
  );
};

const Template: StoryFn<typeof Button> = (args) => <Button {...args} />;

export const Contained = Template.bind({});
Contained.args = {
  variant: "contained",
  children: "CONTAINED",
};

export const Outlined = Template.bind({});
Outlined.args = {
  variant: "outlined",
  children: "OUTLINED",
};

export const Toggle: Story = (args: ButtonProps) => {
  const [active, setActive] = useState(args.active!);

  return (
    <div style={{ display: "flex", gap: "20px" }}>
      <ToggleableButton {...args} active={active} setActive={setActive} />
    </div>
  );
};
Toggle.args = {
  variant: "text",
  size: "compact",
  children: "TOGGLEABLE",
  active: true,
};

export const Text = Template.bind({});
Text.args = {
  variant: "text",
  children: "TEXT",
};

export const Large = Template.bind({});
Large.args = {
  size: "large",
  variant: "outlined",
  children: "LARGE",
};

export const Compact = Template.bind({});
Compact.args = {
  size: "compact",
  variant: "outlined",
  children: "COMPACT",
};
