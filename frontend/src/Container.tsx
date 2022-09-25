export function Container({children}: { children: any }) {
  return <div className="md:mx-20 xl:mx-52 2xl:mx-80">
    {children}
  </div>;
}