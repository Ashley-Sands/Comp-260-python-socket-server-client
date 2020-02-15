using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.AI;

public class MoveAgent : MonoBehaviour
{
    NavMeshAgent myNavMeshAgent;
    public bool followMouse = false;
    Vector3 loc;
    public float stopDist = 1f;
    public float speed = 8;

    void Start ()
    {
        myNavMeshAgent = GetComponent<NavMeshAgent>();
    }

    void Update ()
    {
        if ( followMouse || Input.GetMouseButtonDown( 0 ) )
        {
            SetDestinationToMousePosition();
        }

        if ( Vector3.Distance(transform.position, loc) < stopDist )
        {
            myNavMeshAgent.speed = 0;
        }
        else
        {
            myNavMeshAgent.speed = speed;
        }
    }

    void SetDestinationToMousePosition ()
    {
        RaycastHit hit;
        Ray ray = Camera.main.ScreenPointToRay( Input.mousePosition );
        if ( Physics.Raycast( ray, out hit ) ) 
        {
            myNavMeshAgent.SetDestination( hit.point );
        }

        loc = hit.point;

    }
}
