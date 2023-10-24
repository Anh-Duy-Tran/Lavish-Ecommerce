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
  dragDirection?: "horizontal" | "vertical";
  handleMouseDown: (e: React.MouseEvent<HTMLDivElement>) => void;
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
  handleMouseDown: (e) => {
    if (e.button !== 0) {
      return;
    }

    set(({ mouse }) => ({
      mouse: {
        ...mouse,
        x: e.clientX,
        y: e.clientY,
        offSetX: 0,
        offSetY: 0,
      },
      dragging: true,
      dragDirection: undefined,
    }));
  },
  handleMouseMove: (e) =>
    set(({ dragDirection, dragging, mouse }) => {
      if (!dragging) return {};

      const offset = {
        offSetX: e.clientX - mouse.x,
        offSetY: e.clientY - mouse.y,
      };

      if (
        dragDirection ||
        offset.offSetX * offset.offSetX + offset.offSetY * offset.offSetY < 16
      ) {
        return {
          mouse: {
            ...mouse,
            ...offset,
          },
        };
      }

      return {
        mouse: {
          ...mouse,
          ...offset,
        },
        dragDirection:
          Math.abs(offset.offSetX) >= Math.abs(offset.offSetY) * 0.7
            ? "horizontal"
            : "vertical",
      };
    }),
  handleMouseUp: () =>
    set(() => ({
      dragging: false,
    })),
}));
