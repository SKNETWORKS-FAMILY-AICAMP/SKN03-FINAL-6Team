package com.example.FinalPJ.board.repository;

import com.example.FinalPJ.board.controller.entity.Board;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

@Repository
//<어떤 엔티티를 넣을건지, >
public interface BoardRepository extends JpaRepository<Board, Integer> {
}