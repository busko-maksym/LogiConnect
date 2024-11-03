import React from 'react';
import styles from './Direction.module.css';
import Image, { StaticImageData } from 'next/image';

interface DirectionProps {
    icon: React.ElementType | StaticImageData; 
    title: string;
    description?: string;
    variant?: 'primary' | 'secondary' | 'tertiary';
    selected?: boolean; 
    onClick?: () => void; 
}

const Direction: React.FC<DirectionProps> = ({
    icon,
    title,
    variant = 'primary',
    selected = false,
    onClick
}) => {
    const classNames = `${styles.card} ${styles[variant]} ${selected ? styles.selected : ''}`;

    return (
        <div className={styles.directionWrapper}>
            <button className={classNames} onClick={onClick}>
                <div className={styles.icon}>
                    {typeof icon === 'function' ? (
                        React.createElement(icon)
                    ) : (
                        <Image src={icon} alt={title} width={45} height={45} />
                    )}
                </div>
                <h3 className={styles.title} dangerouslySetInnerHTML={{ __html: title }} />
            </button>
            {selected && <p className={styles.selectedText}>Ви обрали</p>}
        </div>
    );
};

export default Direction;
