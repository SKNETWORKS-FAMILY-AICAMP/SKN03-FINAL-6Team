package com.example.FinalPJ.repository;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import com.example.FinalPJ.entity.BoardEntity;

@Repository
//<어떤 엔티티를 넣을건지, >
public interface BoardRepository extends JpaRepository<BoardEntity, Integer> {
}
