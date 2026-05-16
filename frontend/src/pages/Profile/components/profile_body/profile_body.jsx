import "./profile_body.css"
import { IoMailOutline, IoSaveOutline} from "react-icons/io5";
import { HiOutlineCake } from "react-icons/hi2";


export function ProfileBody({age, email, exercount}) {
    return (
        <>
            <div className="profile-body-content">
                <div className="profile-body-greeting">
  
                    



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