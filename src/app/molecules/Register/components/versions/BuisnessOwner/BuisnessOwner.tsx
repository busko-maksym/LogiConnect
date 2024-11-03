import React, { useState } from 'react';
import styles from './BuisnessOwner.module.css';
import Input from '@/app/atoms/Input/Input';
import axios from 'axios';
import bcrypt from 'bcryptjs';

export default function BuisnessOwner() {
    const [isChecked, setIsChecked] = useState(false);
    const [firstName, setFirstName] = useState('');
    const [lastName, setLastName] = useState('');
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [companyName, setCompanyName] = useState('');
    const [businessType, setBusinessType] = useState('');
    const [companySize, setCompanySize] = useState(0);
    const [cargoTypes, setCargoTypes] = useState('');
    const [logisticsFrequency, setLogisticsFrequency] = useState('');

    const handleCheckBoxChange = () => {
        setIsChecked(!isChecked);
    };

    const handleSubmit = async () => {
        const hashedPassword = bcrypt.hashSync(password, 10); 

        const requestData = {
            first_name: firstName,
            last_name: lastName,
            email: email,
            password: hashedPassword, 
            acc_status: "buisness",
            company_name: companyName,
            business_type: businessType,
            company_size: companySize,
            logistics_frequency: logisticsFrequency,
            cargo_types: cargoTypes.split(',')
        };

        try {
            const response = await axios.post('http://127.0.0.1:8000/user/register/buisness', requestData);
            console.log("Response:", response.data);
        } catch (error) {
            console.error("Error during registration:", error);
        }
    };

    return (
        <div>
            <div className={styles.container_second}>
                <div className={styles.Text}>
                    <h1>Крок №2</h1>
                </div>
                <div className={styles.row}>
                    <div className={styles.column}>
                        <Input 
                            label="Ім’я"
                            placeholder="Ім’я"
                            value={firstName}
                            onChange={(e) => setFirstName(e.target.value)}
                        />
                        <Input 
                            label="Прізвище"
                            placeholder="Прізвище"
                            value={lastName}
                            onChange={(e) => setLastName(e.target.value)}
                        />
                    </div>
                    <div className={styles.column}>
                        <Input 
                            label="Пароль"
                            placeholder="Пароль"
                            type="password"
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                        />
                        <Input
                            label="Електронна пошта"
                            placeholder="Електронна пошта"
                            value={email}
                            onChange={(e) => setEmail(e.target.value)}
                        />
                    </div>
                </div>
            </div>
            <div className={styles.container_third}>
                <div className={styles.Text}>
                    <h1>Крок №3</h1>
                </div>
                <div className={styles.row}>
                    <div className={styles.column}>
                        <Input 
                            label="Назва компанії"
                            placeholder="Назва компанії"
                            value={companyName}
                            onChange={(e) => setCompanyName(e.target.value)}
                        />
                        <Input 
                            label="Тип бізнесу"
                            placeholder="Тип бізнесу"
                            value={businessType}
                            onChange={(e) => setBusinessType(e.target.value)}
                        />
                    </div>
                    <div className={styles.column}>
                        <Input 
                            label="Розмір компанії"
                            placeholder="Розмір компанії"
                            type="number"
                            value={companySize}
                            onChange={(e) => setCompanySize(Number(e.target.value))}
                        />
                        <Input
                            label="Типи вантажів, які зазвичай перевозяться"
                            placeholder="Типи вантажів, які зазвичай перевозяться (через кому)"
                            value={cargoTypes}
                            onChange={(e) => setCargoTypes(e.target.value)}
                        />
                        <Input
                            label="Частота використання логістичних послуг"
                            placeholder="Частота використання логістичних послуг"
                            value={logisticsFrequency}
                            onChange={(e) => setLogisticsFrequency(e.target.value)}
                        />
                    </div>
                </div>
            </div>
            <div className={styles.container_fourth}>
                <div className={styles.Text}>
                    <h1>Крок №4</h1>
                </div>
                <div className={styles.confirm}>
                    <input 
                        type='checkbox'
                        id='terms'
                        checked={isChecked}
                        onChange={handleCheckBoxChange}
                        className={isChecked ? styles.activeInput : styles.inactiveInput}
                    />
                    <label>Я погоджуюсь з умовами використання та політикою <br />конфіденційності</label>
                    <button
                        className={isChecked ? styles.activeButton : styles.disabledButton}
                        onClick={handleSubmit}
                        disabled={!isChecked}
                    >
                        Завершити реєстрацію
                    </button>
                </div>
            </div>
        </div>
    );
}
