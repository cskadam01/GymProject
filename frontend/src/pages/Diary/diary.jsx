import { useState, useEffect } from "react";
import axios from "axios";
import { Link } from "react-router-dom";
import "./diary.css"
import { Navbar } from "../../Navbar/navbar";


export const Diary = () => {
    const [diary, setDiary] = useState([])
 
    useEffect(() => {
        const getUserDiary = async () => {
            try {
               

                const response = await axios.get("http://localhost:8000/diary/user-diary",
                    { withCredentials: true })

                setDiary(response.data)

            }

            catch (err) {


            }
        }
        getUserDiary()

    }, [])

    return (
        <>  
            <Navbar/>
            <div className="diary-conatiner">
                <div className="diary-cont">
                {diary.length === 0 ? (
                    <p>Napló üres</p>

                ) : (
                    diary.map((item) => (
                        <div className="diary-item" key={item.id}>
                            <Link to={`/diary/${item.id}`} key={item.id} style={{textDecoration:"none"}}>
                                <div className="diary-data">
                                <p className="diary-data-name">{item.exer_name}</p>
                                <p className="diary-data-muscle">{item.muscle}</p>
                                <p className="diary-data-type">{item.type}</p>
                                
                                <br />
                                </div>
                            </Link>
                        </div>

                    )

                    ))

                }</div>
            </div>
        </>

    )
}