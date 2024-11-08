'use client'

import React, { useState } from 'react';
import Input from '@/app/atoms/Input/Input';
import axios from 'axios';
import styles from './TruckDriver.module.css';
import bcrypt from 'bcryptjs';
import { useRouter } from 'next/navigation'; 


export default function TruckDriver() {
    const router = useRouter(); 
    const [isChecked, setIsChecked] = useState(false);
    const [firstName, setFirstName] = useState('');
    const [lastName, setLastName] = useState('');
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [licenseType, setLicenseType] = useState('');
    const [licenseNumber, setLicenseNumber] = useState('');
    const [experienceYears, setExperienceYears] = useState(0);
    const [vehicleTypes, setVehicleTypes] = useState([]);
    const [hasPermit, setHasPermit] = useState(false);

    const handleCheckBoxChange = () => {
        setIsChecked(!isChecked);
    };

    const handleSubmit = async () => {
        const hashedPassword = bcrypt.hashSync(password, 10);

        const requestData = {
            first_name: firstName,
            last_name: lastName,
            email: email,
            password: password,
            acc_status: "driver",
            driver_license_type: licenseType,
            driver_license_number: licenseNumber,
            experience_years: experienceYears,
            vehicle_types: vehicleTypes,
            has_international_permit: hasPermit
        };

        console.log("Request data:", requestData); 

        try {
            const response = await axios.post('http://127.0.0.1:8000/user/register/truck', requestData);
            console.log("Response:", response.data);
            router.push('/login'); 
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
                            label="Тип водійських прав"
                            placeholder="Тип водійських прав"
                            value={licenseType}
                            onChange={(e) => setLicenseType(e.target.value)} 
                        />
                        <Input 
                            label="Номер водійського посвідчення"
                            placeholder="Номер водійського посвідчення"
                            value={licenseNumber}
                            onChange={(e) => setLicenseNumber(e.target.value)} 
                        />
                        <Input 
                            label="Досвід роботи (в роках)"
                            placeholder="Досвід роботи (в роках)"
                            value={experienceYears}
                            onChange={(e) => setExperienceYears(Number(e.target.value))}
                        />
                    </div>
                    <div className={styles.column}>
                        <Input
                            label="Типи транспортних засобів, якими можете керувати"
                            placeholder="Типи транспортних засобів, якими можете керувати"
                            value={vehicleTypes}
                            onChange={(e) => setVehicleTypes(e.target.value.split(','))} 
                        />
                        <Input
                            label="Наявність дозволів на міжнародні перевезення"
                            placeholder="Наявність дозволів на міжнародні перевезення"
                            type="checkbox"
                            checked={hasPermit}
                            onChange={(e) => setHasPermit(e.target.checked)} 
                        />
                    </div>
                    <div className={styles.column}>
                        <Input
                            label="Бажані маршрути або регіони роботи"
                            placeholder="Бажані маршрути або регіони роботи"
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
                    >
                        Завершити реєстрацію
                    </button>
                </div>
            </div>
        </div>
    );
}
