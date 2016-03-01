package org.test.samplejee.controller;

import java.util.List;

import javax.annotation.PostConstruct;
import javax.faces.application.FacesMessage;
import javax.faces.bean.ManagedBean;
import javax.faces.context.FacesContext;
import javax.inject.Inject;

import org.test.samplejee.model.Employee;
import org.test.samplejee.service.EmployeeService;

@ManagedBean(name="employeeBean")
public class EmployeeManagedBean {

    @Inject
    private FacesContext facesContext;

    @Inject
    private EmployeeService employeeService;

    private Employee employee;

    @PostConstruct
    public void init() {
        setEmployee(new Employee());
    }

    public void register() throws Exception {
        try {
            employeeService.register(getEmployee());
            FacesMessage m = new FacesMessage(FacesMessage.SEVERITY_INFO, "Registered!", "Registration successful");
            facesContext.addMessage(null, m);
            init();
        } catch (Exception e) {
            FacesMessage m = new FacesMessage(FacesMessage.SEVERITY_ERROR, e.getLocalizedMessage(), "Registration unsuccessful");
            facesContext.addMessage(null, m);
        }
    }

    public Employee getEmployee() {
        return employee;
    }

    public void setEmployee(Employee employee) {
        this.employee = employee;
    }

    public List<Employee> getEmployeeList() {
        return employeeService.list();
    }

}
