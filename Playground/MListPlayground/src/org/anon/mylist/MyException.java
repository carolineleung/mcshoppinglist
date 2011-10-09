package org.anon.mylist;

public class MyException extends RuntimeException {

	private static final long serialVersionUID = -6822206734429855222L;

	public MyException() {
		super();
	}

	public MyException(String detailMessage, Throwable throwable) {
		super(detailMessage, throwable);
	}

	public MyException(String detailMessage) {
		super(detailMessage);
	}

	public MyException(Throwable throwable) {
		super(throwable);
	}

}
