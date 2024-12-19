package com.example.tailorlink.repository;

import com.example.tailorlink.entity.BoardEntity;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

@Repository
//<어떤 엔티티를 넣을건지, >
public interface BoardRepository extends JpaRepository<BoardEntity, Integer> {
}
