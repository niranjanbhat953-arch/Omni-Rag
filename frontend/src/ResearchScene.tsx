import { Canvas } from "@react-three/fiber";
import { Float, OrbitControls, Sparkles } from "@react-three/drei";

function EvidenceNode({ position, color }: { position: [number, number, number]; color: string }) {
  return (
    <Float speed={1.2} rotationIntensity={0.35} floatIntensity={0.55}>
      <mesh position={position}>
        <icosahedronGeometry args={[0.55, 1]} />
        <meshStandardMaterial color={color} emissive={color} emissiveIntensity={0.65} transparent opacity={0.78} />
      </mesh>
    </Float>
  );
}

export function ResearchScene() {
  return (
    <div className="scene" aria-hidden="true">
      <Canvas dpr={[1, 2]} camera={{ position: [0, 0, 6], fov: 46 }}>
        <ambientLight intensity={0.7} />
        <pointLight position={[3, 3, 4]} color="#22d3ee" intensity={14} />
        <pointLight position={[-3, -2, 2]} color="#a855f7" intensity={10} />
        <Sparkles count={90} scale={9} size={1.3} speed={0.25} color="#67e8f9" />
        <EvidenceNode position={[-2, 0.65, -0.4]} color="#22d3ee" />
        <EvidenceNode position={[2, -0.4, -0.2]} color="#a855f7" />
        <EvidenceNode position={[0, 1.55, -0.8]} color="#818cf8" />
        <mesh>
          <sphereGeometry args={[1.05, 32, 32]} />
          <meshStandardMaterial color="#111827" emissive="#22d3ee" emissiveIntensity={0.3} transparent opacity={0.9} />
        </mesh>
        <OrbitControls enableZoom={false} enablePan={false} autoRotate autoRotateSpeed={0.25} />
      </Canvas>
    </div>
  );
}
