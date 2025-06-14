import { useState, useEffect } from "react";
import axios from "axios";
import { Link } from "react-router-dom";


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
            <div className="diary-conatiner">
                {diary.length === 0 ? (
                    <p>Napló üres</p>

                ) : (
                    diary.map((item) => (
                        <div className="diary-item" key={item.id}>
                            <Link to={`/diary/${item.id}`} key={item.id}>
                                <p>{item.exer_name}</p>
                                <p>{item.exer_description}</p>
                                <br />
                            </Link>
                        </div>

                    )

                    ))

                }
            </div>
        </>

    )
}