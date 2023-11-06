import { create } from "zustand";

export type MousePositionType = {
  x: number;
  y: number;
  offSetX: number;
  offSetY: number;
  maxOffSet: number;
};

type MousePositionStore = {
  mouse: MousePositionType;
  dragging: boolean;
  dragDirection?: "horizontal" | "vertical";
  handleMouseDown: (e: React.MouseEvent<HTMLDivElement>) => void;
  handleMouseMove: (e: MouseEvent) => void;
  handleMouseUp: () => void;

  handleTouchStart: (e: React.TouchEvent<HTMLDivElement>) => void;
  handleTouchMove: (e: TouchEvent) => void;
  handleTouchEnd: () => void;
};

const defaultValue: MousePositionType = {
  x: 0,
  y: 0,
  maxOffSet: 0,
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
        maxOffSet: 0,
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
            maxOffSet: Math.max(
              mouse.maxOffSet,
              Math.abs(offset.offSetX),
              Math.abs(offset.offSetY),
            ),
            ...offset,
          },
        };
      }

      return {
        mouse: {
          ...mouse,
          maxOffSet: Math.max(mouse.maxOffSet, offset.offSetX, offset.offSetY),
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

  handleTouchStart(e) {
    set(({ mouse }) => ({
      mouse: {
        ...mouse,
        x: e.touches[0].clientX,
        y: e.touches[0].clientY,
        offSetX: 0,
        offSetY: 0,
        maxOffSet: 0,
      },
      dragging: true,
      dragDirection: undefined,
    }));
  },

  handleTouchMove: (e) =>
    set(({ dragDirection, dragging, mouse }) => {
      e.preventDefault();
      if (!dragging) return {};

      const offset = {
        offSetX: e.touches[0].clientX - mouse.x,
        offSetY: e.touches[0].clientY - mouse.y,
      };

      if (
        dragDirection ||
        offset.offSetX * offset.offSetX + offset.offSetY * offset.offSetY < 16
      ) {
        return {
          mouse: {
            ...mouse,
            maxOffSet: Math.max(
              mouse.maxOffSet,
              Math.abs(offset.offSetX),
              Math.abs(offset.offSetY),
            ),
            ...offset,
          },
        };
      }

      return {
        mouse: {
          ...mouse,
          maxOffSet: Math.max(mouse.maxOffSet, offset.offSetX, offset.offSetY),
          ...offset,
        },
        dragDirection:
          Math.abs(offset.offSetX) >= Math.abs(offset.offSetY) * 0.7
            ? "horizontal"
            : "vertical",
      };
    }),

  handleTouchEnd: () =>
    set(() => ({
      dragging: false,
    })),
}));
