package main

import (
	"fmt"
	"net"
	"bufio"
	"io"
	// "sync"
)

type Conn struct {
	tcpConn *net.TCPConn
	closed  bool
	reader  *bufio.Reader
}

func GetConn(host string, port int) (*Conn, error){
	tcpAddr, err := net.ResolveTCPAddr("tcp4", fmt.Sprintf("%s:%d", host, port))
	if err != nil {
		return nil, err
	}

	tcpConn, err := net.DialTCP("tcp4", nil, tcpAddr)
	if err != nil {
		return nil, err
	}
	conn := &Conn{
		tcpConn: tcpConn,
		closed: false,
		reader: bufio.NewReader(tcpConn),
	}
	return conn, nil
}

func NewConn(tcpConn *net.TCPConn) (*Conn, error) {
	c := &Conn{}
	if tcpConn == nil {
		return c, fmt.Errorf("get tcpConn nil")
	}
	c.tcpConn = tcpConn
	c.reader = bufio.NewReader(tcpConn)
	c.closed = false
	return c, nil
}

func (conn*Conn) Close() error {
	return conn.tcpConn.Close()
}

func (conn*Conn) Write(data []byte) (int, error) {
	return conn.tcpConn.Write(data)
}

//If ReadLineB encounters an error before reaching '\n', it returns the data read before the error and the error itself (often io.EOF). 
func (conn*Conn) ReadLineB() ([]byte, error) {
	data, err := conn.reader.ReadBytes('\n')
	if err != nil {
		return data, err
	}
	return data, nil
}

func (conn*Conn) GetReader() (*bufio.Reader, error) {
	if conn.reader != nil {
		return conn.reader, nil
	}
	if conn.tcpConn == nil {
		return nil, fmt.Errorf("Get reader failed: TCPConn doesn't exist")
	}
	conn.reader = bufio.NewReader(conn.tcpConn)
	return conn.reader, nil
}

func (conn*Conn) RemoteAddr() net.Addr {
	return conn.tcpConn.RemoteAddr()
}

func Forward(from *Conn, to *Conn) {
	io.Copy(to.tcpConn, from.tcpConn)
}



func main() {
	// c, err := GetConn("cn-fz-dx.sakurafrp.com", 41598)
	// c, err := GetConn("127.0.0.1", 2000)
	c, err := GetConn("120.77.80.177", 4000)
	if err != nil {
		fmt.Printf("connect to server error")
	}
	defer c.Close()
	c.Write([]byte("message from client"))
	data, err := c.ReadLineB()
	fmt.Println(string(data))
}











