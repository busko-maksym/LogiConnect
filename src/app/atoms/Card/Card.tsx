import React from 'react';
import styles from './Card.module.css';
import Image, { StaticImageData } from 'next/image';

interface CardProps {
    icon: React.ElementType | StaticImageData; 
    title: string;
    description?: string;
    variant?: 'primary' | 'secondary' | 'tertiary';
}

const Card: React.FC<CardProps> = ({
    icon,
    title,
    description,
    variant = 'primary'
}) => {
    const classNames = `${styles.card} ${styles[variant]}`;

    return (
        <div className={classNames}>
            <div className={styles.icon}>
                {typeof icon === 'function' ? (
                    React.createElement(icon)
                ) : (
                    <Image src={icon} alt={title} width={50} height={50} />
                )}
            </div>
            <h3 className={styles.title} dangerouslySetInnerHTML={{ __html: title }} />
            {description && (
                <p className={styles.description} dangerouslySetInnerHTML={{ __html: description }} />
            )}
        </div>
    );
}

export default Card;
