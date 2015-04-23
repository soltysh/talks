package org.test.samplejee.service;

import java.util.List;

import org.test.samplejee.model.Employee;

public interface EmployeeService {

    void register(Employee employee) throws Exception;

    List<Employee> list();

}
