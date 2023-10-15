import type { Meta, StoryObj } from "@storybook/react";
import Mainpage from "./page";

const meta = {
  title: "Pages/Mainpage",
  component: Mainpage,
} satisfies Meta<typeof Mainpage>;

export default meta;
type Story = StoryObj<typeof meta>;

export const Primary: Story = {};
