package org.test.samplejee.dao;

import java.util.List;

import java.util.logging.Logger;

import javax.ejb.Stateless;
import javax.inject.Inject;
import javax.persistence.EntityManager;

import org.test.samplejee.model.Employee;

@Stateless
public class EmployeeDAOImpl implements EmployeeDAO {

    @Inject
    private Logger log;

    @Inject
    private EntityManager em;


    @Override
    public void register(Employee employee) throws Exception {
        log.info("Registering " + employee.getLabel());
        em.persist(employee);
    }

    @Override
    public List<Employee> list() {
        return em.createQuery("SELECT e FROM Employee e").getResultList();
    }
}
