import React from "react";
import type { ComponentStory, Meta, StoryFn, StoryObj } from "@storybook/react";
import { ButtonProps, Button } from "./Button";
import { useState } from "react";

const meta = {
  title: "Assets/Button",
  component: Button,
  parameters: {
    layout: "centered",
  },
  tags: ["autodocs"],
  argTypes: {},
} satisfies Meta<typeof Button>;

export default meta;
type Story = StoryObj<typeof meta>;

// const ToggleableButton = ({
//   active,
//   setActive,
//   ...props
// }: ButtonProps & {
//   active: boolean;
//   setActive: React.Dispatch<React.SetStateAction<boolean>>;
// }) => {
//   return (
//     <Button
//       {...props}
//       active={active}
//       onClick={() => setActive((prev) => !prev)}
//     />
//   );
// };

const Template: StoryFn<typeof Button> = (args) => <Button {...args} />;

export const Contained = Template.bind({});
Contained.args = {
  variant: "contained",
  label: "Contained",
};

export const Outlined = Template.bind({});
Outlined.args = {
  variant: "outlined",
  label: "Outlined",
}
// export const Outlined: Story = {
//   args: {
//     variant: "outlined",
//     label: "Outlined",
//   },
// };

// export const Toggle: Story = (args: ButtonProps) => {
//   const [active, setActive] = useState(false);

//   return (
//     <div style={{ display: "flex", gap: "20px" }}>
//       <ToggleableButton
//         {...args}
//         active={active}
//         setActive={setActive}
//         variant="outlined"
//       />
//       <ToggleableButton {...args} active={active} setActive={setActive} />
//     </div>
//   );
// };
// Toggle.args = {
//   variant: "text",
//   size: "large",
//   label: "Toggleable",
//   active: false,
// };

// export const Text: Story = {
//   args: {
//     variant: "text",
//     label: "Text",
//   },
// };

// const widths = [100, 200, 400];
// export const VariesWidth: Story = {
//   render: () => {
//     return (
//       <div style={{ display: "flex", gap: "10px" }}>
//         {widths.map((width) => (
//           <Button
//             variant="contained"
//             width={width}
//             key={width}
//             label={`${width}px`}
//           />
//         ))}
//       </div>
//     );
//   },
// };

// export const FullWidth: Story = {
//   render: () => {
//     return (
//       <>
//         <p>Container</p>
//         <div
//           style={{ width: "500px", padding: "10px", border: "1px solid black" }}
//         >
//           <Button variant="contained" fullWidth label="Full Width" />
//         </div>
//       </>
//     );
//   },
// };

// export const Large: Story = {
//   args: {
//     size: "large",
//     label: "Button",
//   },
// };

// export const Compact: Story = {
//   args: {
//     variant: "text",
//     size: "compact",
//     label: "Small",
//   },
// };
