import FooterInfo from '@/app/molecules/FooterInfo/FooterInfo';
import React from 'react';

type FooterProps = {
  className?: string; // Пропс для задания отступа сверху
};

const Footer: React.FC<FooterProps> = ({ className }) => {
  return (
    <div className={className}>
      <FooterInfo />
    </div>
  );
};

export default Footer;