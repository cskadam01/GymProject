import "./profile_body.css"
import { IoMailOutline, IoSaveOutline} from "react-icons/io5";
import { HiOutlineCake } from "react-icons/hi2";


export function ProfileBody({age, email, exercount}) {
    return (
        <>
            <div className="profile-body-content">
                <div className="profile-body-greeting">
                    <h3 >Az appról</h3>
                    <p>Ez az a webalkalmazást azért hoztam létre, mert szerettem volna egy appot ahol
                        nyomon tudom követni a konditermi fejlődésem. </p>

                    <p>Továbbá programozás terén is jó tanulási lehetőségnek tartom. Így nem kellet előfizetnem egy appra, hanem csináltam
                        egy sajátot

                    </p>
                    <p>Ez az oldal első sorban telefonos felhasználásra lett tervezve, de számítógépen is rendesen fog futni, ez késöbbi frissítésekben fog változni</p>
                    <p>Bármilyen észrevétel nagyon sokat tud segíteni a lenti
                        lehetőségeken kérlek vedd fel velem a kapcsolatot és egyeztetünk </p>


                    <p>verzió szám: 0.1 alpha
                    </p>

                    



                </div>

                <div className="profile-body-contacts">
                    <div className="profile-body-contacts-cont">
                    <h3>Adataid</h3>
                    <p><IoMailOutline style={{marginRight:"8px"}}/>{email}</p>
                    <p><HiOutlineCake /> {age} éves</p>  
                    <p><IoSaveOutline /> {exercount} naplózott feladat</p>
                    
                </div>


                </div>

            </div>
        </>


    )



}