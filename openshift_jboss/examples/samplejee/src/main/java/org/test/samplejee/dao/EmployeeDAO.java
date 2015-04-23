package org.test.samplejee.dao;

import java.util.List;

import org.test.samplejee.model.Employee;

public interface EmployeeDAO {

    void register(Employee employee) throws Exception;

    List<Employee> list();

}
