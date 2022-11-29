import {FunctionComponent, PropsWithChildren} from 'react';
export const Container: FunctionComponent<PropsWithChildren> = ({children}) => {
  return <div className="md:mx-20 xl:mx-52 2xl:mx-80">{children}</div>;
};
