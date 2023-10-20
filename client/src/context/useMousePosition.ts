import { create } from "zustand";

export type MousePositionType = {
  x: number;
  y: number;
  offSetX: number;
  offSetY: number;
};

type MousePositionStore = {
  mouse: MousePositionType;
  dragging: boolean;
  handleMouseDown: (e: React.MouseEvent<HTMLUListElement>) => void;
  handleMouseMove: (e: MouseEvent) => void;
  handleMouseUp: () => void;
};

const defaultValue: MousePositionType = {
  x: 0,
  y: 0,
  offSetX: 0,
  offSetY: 0,
};

export const useMousePosition = create<MousePositionStore>()((set) => ({
  mouse: defaultValue,
  dragging: false,
  handleMouseDown: (e) =>
    set(({ mouse }) => ({
      mouse: {
        ...mouse,
        x: e.clientX,
        y: e.clientY,
      },
      dragging: true,
    })),
  handleMouseMove: (e) =>
    set(({ dragging, mouse }) => {
      if (!dragging) return {};
      return {
        mouse: {
          ...mouse,
          offSetX: e.clientX - mouse.x,
          offSetY: e.clientY - mouse.y,
        },
      };
    }),
  handleMouseUp: () =>
    set(() => ({
      mouse: defaultValue,
      dragging: false,
    })),
}));
