import Image from "next/image";

export default function Twiggy() {
  return (
    <div className="h-screen w-screen bg-gradient-to-tr from-lime-100 to-emerald-100">
      <div className="flex flex-col items-center h-full">
        <div className = "p-10 lg:text-6xl md:text-5xl text-5xl font-semibold text-center lg:pb-5 md:pb-3 pb-1">Twiggy</div>
        <div className = "h-full w-10/12 mb-10 mt-5 border-black rounded-xl border-4"></div>
      </div>
    </div>
  );
}
