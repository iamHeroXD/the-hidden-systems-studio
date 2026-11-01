import {makeScene2D, createRef, all, easeInOutCubic} from '@motion-canvas/2d';
import {Circle, Rect, Txt, Node, Camera} from '@motion-canvas/2d';

export default makeScene2D(function* (view) {
  const camera = createRef<Camera>();
  const title = createRef<Txt>();
  const filament = createRef<Rect>();

  view.add(
    <Camera ref={camera}>
      <Rect
        width={1920}
        height={1080}
        fill={'#0B0F17'}
      />
      <Rect
        ref={filament}
        width={800}
        height={8}
        fill={'#06B6D4'}
        radius={4}
      />
      <Txt
        ref={title}
        text={'THE HIDDEN SYSTEMS'}
        fontFamily={'monospace'}
        fontSize={48}
        fill={'#E2E8F0'}
        y={120}
        opacity={0}
      />
    </Camera>
  );

  yield* all(
    filament().scale.x(1.5, 2.0, easeInOutCubic),
    title().opacity(1, 1.5),
    camera().zoom(1.15, 3.0, easeInOutCubic)
  );
});
