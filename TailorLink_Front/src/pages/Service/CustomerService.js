// import React, { useState } from "react";

// const Service = () => {
//   const [isPopupVisible, setIsPopupVisible] = useState(false);

//   const togglePopup = () => {
//     setIsPopupVisible(!isPopupVisible);
//   };

//   return (
//     <div style={styles.container}>
//       <h1 style={styles.title}>고객센터</h1>
//       <p style={styles.description}>소중한 고객님의 목소리를 귀담아 듣는 테일러링크가 되겠습니다.</p>

//       <button onClick={togglePopup} style={styles.button}>
//         고객센터 보기
//       </button>

//       {isPopupVisible && (
//         <div style={styles.popup}>
//           <div style={styles.popupContent}>
//             <h2>문의하기</h2>
//             <ul>
//               <li>게시판</li>
//               <li>찾아오는 길</li>
//             </ul>
//             <button onClick={togglePopup} style={styles.closeButton}>
//               닫기
//             </button>
//           </div>
//         </div>
//       )}
//     </div>
//   );
// };

// const styles = {
//   container: {
//     padding: "20px",
//     textAlign: "center",
//   },
//   title: {
//     fontSize: "2rem",
//     fontWeight: "bold",
//     marginBottom: "10px",
//   },
//   description: {
//     fontSize: "1rem",
//     color: "#555",
//     marginBottom: "20px",
//   },
//   button: {
//     padding: "10px 20px",
//     backgroundColor: "#4A90E2",
//     color: "#fff",
//     border: "none",
//     borderRadius: "5px",
//     cursor: "pointer",
//   },
//   popup: {
//     position: "fixed",
//     top: "0",
//     left: "0",
//     width: "100%",
//     height: "100%",
//     backgroundColor: "rgba(0, 0, 0, 0.5)",
//     display: "flex",
//     justifyContent: "center",
//     alignItems: "center",
//   },
//   popupContent: {
//     backgroundColor: "#fff",
//     padding: "20px",
//     borderRadius: "10px",
//     textAlign: "center",
//     width: "300px",
//   },
//   closeButton: {
//     marginTop: "20px",
//     padding: "10px 20px",
//     backgroundColor: "#ff5c5c",
//     color: "#fff",
//     border: "none",
//     borderRadius: "5px",
//     cursor: "pointer",
//   },
// };

// export default Service;