import { Suspense } from "react";
import { Canvas } from "@react-three/fiber";
import { OrbitControls, useGLTF } from "@react-three/drei";

function Model() {
  const { scene } = useGLTF(`${import.meta.env.BASE_URL}models/smoke_test.glb`);
  return <primitive object={scene} />;
}

export default function App() {
  return (
    <div style={{ width: "100vw", height: "100vh" }}>
      <Canvas camera={{ position: [350, 250, 350], fov: 45, near: 1, far: 5000 }}>
        <color attach="background" args={["#14161a"]} />
        <ambientLight intensity={0.6} />
        <directionalLight position={[300, 500, 200]} intensity={1.6} />
        <Suspense fallback={null}>
          <Model />
        </Suspense>
        <gridHelper args={[600, 30, "#444", "#2a2a2a"]} position={[0, -81, 0]} />
        <OrbitControls makeDefault />
      </Canvas>
    </div>
  );
}