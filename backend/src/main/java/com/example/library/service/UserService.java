package com.example.library.service;

import com.example.library.common.service.BaseService;
import com.example.library.pojo.dto.LoginDTO;
import com.example.library.pojo.entity.User;
import com.example.library.pojo.vo.LoginVO;
import com.example.library.pojo.dto.RegisterDTO;

/**
 * @author WangYi
 * @create 2024/7/30
 */
public interface UserService extends BaseService<User> {
    /**
     * 登陆
     * @param loginDTO
     * @return
     */
    LoginVO login(LoginDTO loginDTO);
    // UserService.java 新增方法
    Boolean register(RegisterDTO dto);
}

