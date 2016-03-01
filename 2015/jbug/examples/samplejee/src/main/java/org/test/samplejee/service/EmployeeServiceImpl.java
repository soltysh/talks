package org.test.samplejee.service;

import java.util.List;
import java.util.logging.Logger;

import javax.ejb.Stateless;
import javax.inject.Inject;

import org.test.samplejee.dao.EmployeeDAO;
import org.test.samplejee.model.Employee;

@Stateless
public class EmployeeServiceImpl implements EmployeeService {

    @Inject
    private Logger log;

    @Inject
    private EmployeeDAO dao;

    @Override
    public void register(Employee employee) throws Exception {
        log.info("Registering " + employee.getLabel());
        dao.register(employee);
    }

    @Override
    public List<Employee> list() {
        return dao.list();
    }
}
