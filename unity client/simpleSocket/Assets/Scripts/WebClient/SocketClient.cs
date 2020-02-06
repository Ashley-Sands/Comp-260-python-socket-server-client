using System.Text;
using System.Net;
using System.Net.Sockets;
using System.Threading;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class SocketClient : MonoBehaviour
{

    private ASCIIEncoding encoder = new ASCIIEncoding();
    private byte[] buffer = new byte[ 1024 ];

    private Socket socket = new Socket( AddressFamily.InterNetwork, SocketType.Stream, ProtocolType.Tcp );

    private readonly string hostIp = "192.168.0.1";
    private readonly int port = 8222;

    private Thread receiveThread;
    private bool reciveThread_isRunning = true;

    // Start is called before the first frame update
    void Start()
    {

        socket.Connect( new IPEndPoint( IPAddress.Parse(hostIp), port ) );

    }

    // Update is called once per frame
    void Update()
    {
        
    }

    private void ReciveMessage()
    {

        while (reciveThread_isRunning)
        {
            
            

        }

    }

}
