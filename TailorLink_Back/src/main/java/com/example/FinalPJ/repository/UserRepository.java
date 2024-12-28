package com.example.FinalPJ.repository;

import com.example.FinalPJ.entity.UserEntity;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.Optional;

@Repository
public interface UserRepository extends JpaRepository<UserEntity, String> {
    boolean existsByUserId(String userId);
    boolean existsByEmail(String email);
    boolean existsByName(String name);
    boolean existsByPhoneNumber(String phoneNumber);

    UserEntity findByUserId(String userId);

    Optional<UserEntity> findByNameAndEmail(String name, String email);

}
