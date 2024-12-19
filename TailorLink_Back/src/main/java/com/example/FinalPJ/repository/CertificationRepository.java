package com.example.FinalPJ.repository;

import jakarta.transaction.Transactional;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import com.example.FinalPJ.entity.CertificationEntity;

@Repository
public interface CertificationRepository extends JpaRepository<CertificationEntity, String> {

    // certificationEntity 반환하는 findByMemberId 만듬
    CertificationEntity findByUserId(String userId);

    @Transactional
    void deleteByUserId(String userId);
}
