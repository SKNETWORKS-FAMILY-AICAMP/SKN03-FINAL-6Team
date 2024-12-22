import React from "react";
import "./FirstSection.css";
import mainImage from "../../../assets/images/AICFN.png";

const FirstSection = ({ stage }) => {
  return (
    <div className={`first-section ${stage === 0 ? "visible" : "hidden"}`}>
      <img src={mainImage} alt="AICFN" className="main-image" />
    </div>
  );
};

export default FirstSection;
